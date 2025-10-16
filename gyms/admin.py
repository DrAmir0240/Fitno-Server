from django.contrib import admin
from gyms.models import Gym, MemberShipType, MemberShip, Closet, InOut, BlockList, Rate, GymBanner, GymImage, \
    GymSecretary


# Register your models here.
@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(GymBanner)
class GymBannerAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(GymImage)
class GymImageAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(GymSecretary)
class GymSecretaryAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(MemberShipType)
class MemberShipTypeAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(MemberShip)
class MemberShipAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(Closet)
class ClosetAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(InOut)
class InOutAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(BlockList)
class BlockListAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'
