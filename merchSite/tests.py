from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Cart, Product, Order, ReturnProduct
import json

class ClassMergeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Testing@123')
        self.product = Product.objects.create(name = 'Test Product', 
                                            price = 1700, 
                                            size_options = '{"L": 2, "M": 3, "S": 2}',
                                            description = "Test Product being tested."
                                        )
     
        self.client = Client()

    def test_guest_to_user_emerge(self):
        session = self.client.session
        session.create()
        guest_session_key = session.session_key

        Cart.objects.create(
            session_id = guest_session_key,
            product = self.product,
            size = 'M',
            quantity = 2
        )
        self.assertTrue(Cart.objects.filter(session_id = guest_session_key).exists())
        login_response = self.client.login(username = 'testuser', password ='Testing@123')
        Cart.objects.update(user = self.user)
        self.assertFalse(Cart.objects.filter(session_id = guest_session_key).exists())
        user_cart = Cart.objects.filter(user = self.user , product= self.product, size = 'M').first()
        self.assertIsNotNone(user_cart)
        self.assertEqual(user_cart.quantity , 2)
        print("\n✅ Test Passed: Guest Cart successfully merged to User Account!")

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



class ProductTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name = "Black Leggins",
            price = "2500",
            size_options = {
                "L" : 1,
                "M": 0,
                "S": 1
            }
        )

    def test_merge_quantities(self):
        self.assertEqual(self.product.total_quantity , 2)
        print("\n✅ Test Passed: The total quantities are merged correctly!")

class AddingToCartTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Testing@123')
        self.product = Product.objects.create(
            name = "Black Leggins",
            price = "2500",
            size_options = {
                "L" : 2,
                "M": 0,
                "S": 1
            }
        )
        self.add_to_cart_url = reverse("add_to_cart", args = [self.product.id])

    # def test_adding_non_existant_product_to_cart(self):
    #     response = self.client.post(self.add_to_cart_url, {'size' : 'M'})
    #     self.assertEqual(response.status_code, 400)
    #     print("Test Passed")

    def test_adding_existant_product_to_cart(self):
        print(f"URL: {self.add_to_cart_url}")
        print(f"Product ID: {self.product.id}")
        response = self.client.post(self.add_to_cart_url, {'size' : 'L'}, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Added this item to your bag. To view it click here! ')
        print("Test Passed")


    def test_negative_quantity_in_cart(self):
        response = self.client.post(self.add_to_cart_url, {'size' : 'L', 'quantity' : -1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quantity cannot be negative!")

        from . models import Cart
        self.assertFalse(Cart.objects.filter(product= self.product, size = 'L').exist())
        print("Test Passed")


    
        
    
