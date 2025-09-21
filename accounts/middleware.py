from django.utils.deprecation import MiddlewareMixin
import time
from django.core.cache import cache
from django.http import JsonResponse

from accounts.models import APIKey


class APIKeyMiddleware:
    EXEMPT_PATHS = [
        "/admin/",
        "/schema/",
        "/swagger/",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر مسیر جزو استثناها بود → چک API Key انجام نشه
        for exempt in self.EXEMPT_PATHS:
            if request.path.startswith(exempt):
                return self.get_response(request)

        # گرفتن API Key از هدر
        api_key = request.headers.get("x-api-key")
        if not api_key:
            return JsonResponse({"detail": "API Key missing."}, status=403)

        # بررسی اعتبار کلید
        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            return JsonResponse({"detail": "Invalid or inactive API Key."}, status=403)

        return self.get_response(request)


class GlobalRateLimitMiddleware:
    RATE_LIMIT = 1000  # حداکثر ریکوئست
    TIME_WINDOW = 3600  # بازه زمانی (ثانیه = یک ساعت)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # کلید یکتا برای هر کاربر (ترجیحا بر اساس IP یا user.id)
        if hasattr(request, 'user') and request.user.is_authenticated:
            ident = f"user_{request.user.id}"
        else:
            ident = f"ip_{self.get_client_ip(request)}"

        # گرفتن تعداد درخواست‌ها از کش
        cache_key = f"rate_limit_{ident}"
        data = cache.get(cache_key, {"count": 0, "start_time": time.time()})

        # بررسی اینکه آیا بازه یک ساعته گذشته یا نه
        elapsed = time.time() - data["start_time"]
        if elapsed > self.TIME_WINDOW:
            data = {"count": 0, "start_time": time.time()}

        # افزایش شمارش
        data["count"] += 1

        # اگر بیشتر از حد مجاز → خطای 429
        if data["count"] > self.RATE_LIMIT:
            return JsonResponse(
                {"detail": "Rate limit exceeded. Try again later."},
                status=429
            )

        # ذخیره دوباره در کش
        cache.set(cache_key, data, timeout=self.TIME_WINDOW)

        return self.get_response(request)

    def get_client_ip(self, request):
        """استخراج IP کلاینت (در صورت عدم لاگین)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
