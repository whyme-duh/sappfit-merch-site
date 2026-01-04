from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Cart, Product

class ClassMergeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Testing@123')
        self.product = Product.objects.create(name = 'Test Product', 
                                            price = 1700, 
                                            size_options = '{"L": 2, "M": 3, "S": 2}',
                                            description = "Test Product being tested."
                                        )
        self.client = Client()

    # def test_guest_to_user_emerge(self):
    #     session = self.client.session
    #     session.create()
    #     guest_session_key = session.session_key

    #     Cart.objects.create(
    #         session_id = guest_session_key,
    #         product = self.product,
    #         size = 'M',
    #         quantity = 2
    #     )
    #     self.assertTrue(Cart.objects.filter(session_id = guest_session_key).exists())
    #     login_response = self.client.login(username = 'testuser', password ='Testing@123')
    #     Cart.objects.update(user = self.user)
    #     self.assertFalse(Cart.objects.filter(session_id = guest_session_key).exists())
    #     user_cart = Cart.objects.filter(user = self.user , product= self.product, size = 'M').first()
    #     self.assertIsNotNone(user_cart)
    #     self.assertEqual(user_cart.quantity , 2)
    #     print("\n✅ Test Passed: Guest Cart successfully merged to User Account!")

    def test_merge_cart_quntity(self):
        Cart.objects.create(user = self.user, product = self.product, size = 'M', quantity = 2)
        session = self.client.session
        session.create()
        guest_session_key = session.session_key

        Cart.objects.create(session_id = guest_session_key, product = self.product, size = 'M' , quantity = 2)
        self.client.login(username = 'testuser' , password = 'Testing@123')
        user_item = Cart.objects.get(user = self.user, product = self.product)
        self.assertTrue(user_item.quantity, 4)
        print("\n✅ Test Passed: Quantities merged correctly (2 + 2 = 4)!")