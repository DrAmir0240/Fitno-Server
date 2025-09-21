"""
this file contains all db tables for all phase
"""
# # 1. User (if you use a custom user, this can be skipped)
# class UserProfile(BaseModel):
#     phone_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(blank=True, null=True)
#     otp = models.CharField(max_length=10, blank=True, null=True)
#     password = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.email or self.phone_number
#
# # 2. GymSecretary
# class GymSecretary(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_secretaries')
#     full_name = models.CharField(max_length=255)
#     national_code = models.CharField(max_length=50, blank=True, null=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     gym = models.ForeignKey('Gym', on_delete=models.SET_NULL, null=True, blank=True, related_name='secretaries')
#     employee_code = models.CharField(max_length=100, blank=True, null=True)
#     permissions = models.JSONField(blank=True, null=True)
#
#     def __str__(self):
#         return self.full_name
#
# # 3. GymManager
# class GymManager(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_managers')
#     full_name = models.CharField(max_length=255)
#     national_code = models.CharField(max_length=50, blank=True, null=True)
#     verification_code = models.CharField(max_length=100, blank=True, null=True)
#     company_title = models.CharField(max_length=255, blank=True, null=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     city = models.CharField(max_length=255, blank=True, null=True)
#     invitation_code = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.full_name
#
# # 4. Customer
# class Customer(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
#     full_name = models.CharField(max_length=255)
#     national_code = models.CharField(max_length=50, blank=True, null=True)
#     city = models.CharField(max_length=255, blank=True, null=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
#
#     def __str__(self):
#         return self.full_name
#
# # 5. Admin
# class Admin(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admins')
#     full_name = models.CharField(max_length=255)
#     access_code = models.CharField(max_length=100)
#     password = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.full_name
#
# # 6. Seller
# class Seller(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sellers')
#     full_name = models.CharField(max_length=255)
#     national_code = models.CharField(max_length=50, blank=True, null=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     verification_code = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.full_name
#
# # 7. GymCoach
# class GymCoach(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_coaches')
#     full_name = models.CharField(max_length=255)
#     national_code = models.CharField(max_length=50, blank=True, null=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     gym = models.ForeignKey('Gym', on_delete=models.SET_NULL, null=True, blank=True, related_name='coaches')
#
#     def __str__(self):
#         return self.full_name
#
# # 8. PlatformManager
# class PlatformManager(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='platform_managers')
#     full_name = models.CharField(max_length=255)
#     access_code = models.CharField(max_length=100)
#     password = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.full_name
#
# # 9. Marketer
# class Marketer(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketers')
#     full_name = models.CharField(max_length=255)
#     access_code = models.CharField(max_length=100, blank=True, null=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     referral_code = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.full_name
#
# # 10. Gym
# class Gym(BaseModel):
#     title = models.CharField(max_length=255)
#     address = models.TextField(blank=True, null=True)
#     manager = models.ForeignKey(GymManager, on_delete=models.SET_NULL, null=True, blank=True, related_name='gyms')
#     location = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=50, blank=True, null=True)
#     headline_phone = models.CharField(max_length=50, blank=True, null=True)
#     session_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
#     session_days = models.IntegerField(default=0)
#     commission_type = models.CharField(max_length=50, blank=True, null=True)
#     facilities = models.JSONField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     work_hours_per_day = models.CharField(max_length=100, blank=True, null=True)
#     one_day_session_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
#
#     def __str__(self):
#         return self.title
#
# # 11. Store
# class Store(BaseModel):
#     title = models.CharField(max_length=255)
#     seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, related_name='stores')
#     address = models.TextField(blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=50, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
# # 12. (Possibly Subscription / Membership) - named Transaction-like fields were present in the diagram
# class Subscription(BaseModel):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
#     start_date = models.DateField(null=True, blank=True)
#     validity_date = models.DateField(null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     transaction = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
#     days = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"Subscription {self.unique_id} - {self.customer}"
#
# # 13. Closet
# class Closet(BaseModel):
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='closets')
#     number = models.CharField(max_length=100)
#     status = models.CharField(max_length=50, default='available')
#
#     def __str__(self):
#         return f"{self.gym.title} - {self.number}"
#
# # 14. InOut (entry/exit log)
# class InOut(BaseModel):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='inouts')
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='inouts')
#     closet = models.ForeignKey(Closet, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
#     enter_time = models.DateTimeField(null=True, blank=True)
#     out_time = models.DateTimeField(null=True, blank=True)
#     confirm_in = models.BooleanField(default=False)
#     session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
#
#     def __str__(self):
#         return f"InOut {self.customer} @ {self.gym}"
#
# # 15. Product
# class Product(BaseModel):
#     title = models.CharField(max_length=255)
#     balance = models.IntegerField(default=0)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
#     sold_count = models.IntegerField(default=0)
#     category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
#
#     def __str__(self):
#         return self.title
#
# # 16. ShoppingItem
# class ShoppingItem(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shopping_items')
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, related_name='items')
#
#     def __str__(self):
#         return f"{self.product} x {self.quantity}"
#
# # 17. ExerciseCategory
# class ExerciseCategory(BaseModel):
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='exercise_categories/', blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
# # 18. ShoppingCart
# class ShoppingCart(BaseModel):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shopping_carts')
#     total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#
#     def __str__(self):
#         return f"Cart {self.customer} - {self.total_price}"
#
# # 19. Exercise
# class Exercise(BaseModel):
#     title = models.CharField(max_length=255)
#     video = models.URLField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_exercises')
#     exercise_category = models.ForeignKey(ExerciseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='exercises')
#
#     def __str__(self):
#         return self.title
#
# # 20. Category (for store/products)
# class Category(BaseModel):
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
# # 21. WorkoutPlan
# class WorkoutPlan(BaseModel):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='workout_plans')
#     gym_coach = models.ForeignKey(GymCoach, on_delete=models.SET_NULL, null=True, blank=True, related_name='workout_plans')
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     description = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f"Plan for {self.customer}"
#
# # 22. WorkoutDay
# class WorkoutDay(BaseModel):
#     title = models.CharField(max_length=255)
#     workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='days')
#
#     def __str__(self):
#         return self.title
#
# # 23. PlanExercise
# class PlanExercise(BaseModel):
#     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='plan_exercises')
#     quantity = models.IntegerField(default=1)
#     set_count = models.IntegerField(default=1)
#     workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='plan_exercises')
#
#     def __str__(self):
#         return f"{self.exercise} - {self.workout_day}"
#
# # 24. Transaction
# class Transaction(BaseModel):
#     payer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_paid')
#     receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions_received')
#     payment_method = models.CharField(max_length=100, blank=True, null=True)
#     online_transaction = models.CharField(max_length=255, blank=True, null=True)
#     price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#
#     def __str__(self):
#         return f"Tx {self.unique_id} - {self.price}"
#
# # 25. Order
# class Order(BaseModel):
#     item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
#     price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     description = models.TextField(blank=True, null=True)
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
#     transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
#
#     def __str__(self):
#         return f"Order {self.unique_id}"
#
# # 26. Ticket
# class Ticket(BaseModel):
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_tickets')
#     message = models.TextField()
#     send_time = models.DateTimeField(auto_now_add=True)
#     replied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
#
#     def __str__(self):
#         return f"Ticket {self.unique_id} from {self.sender}"
#
# # 27. BlockList
# class BlockList(BaseModel):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='blocked_gyms')
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='blocked_by')
#     description = models.TextField(blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.customer} blocked {self.gym}"
#
# # 28. Notification
# class Notification(BaseModel):
#     action = models.CharField(max_length=255)
#     message = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     is_read = models.BooleanField(default=False)
#     meta = models.JSONField(blank=True, null=True)
#
#     def __str__(self):
#         return f"Notification for {self.user}"
#
# # 29. Announcements
# class Announcement(BaseModel):
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
#     type = models.CharField(max_length=100, blank=True, null=True)
#     message = models.TextField()
#
#     def __str__(self):
#         return f"Announcement {self.unique_id}"
#
# # 30. Rate
# class Rate(BaseModel):
#     rate = models.PositiveSmallIntegerField()
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rates')
#     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='rates')
#
#     def __str__(self):
#         return f"{self.rate} by {self.customer} for {self.gym}"
#
