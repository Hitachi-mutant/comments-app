# from rest_framework import serializers
# from .models import Comment

# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url

# class CommentSerializer(serializers.ModelSerializer):
#     captcha_key = serializers.CharField(write_only=True)
#     captcha_value = serializers.CharField(write_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'name', 'email', 'homepage', 'text', 'file', 'created_at', 'parent', 'captcha_key', 'captcha_value']
#         read_only_fields = ['id', 'created_at', 'parent'] 

#     def validate(self, data):
#         captcha_key = data.pop('captcha_key', None)
#         captcha_value = data.pop('captcha_value', None)

#         if not captcha_key or not captcha_value:
#             raise serializers.ValidationError("CAPTCHA is required.")

#         try:
#             captcha = CaptchaStore.objects.get(hashkey=captcha_key)
#         except CaptchaStore.DoesNotExist:
#             raise serializers.ValidationError("Invalid CAPTCHA key.")

#         if captcha.response != captcha_value.strip().lower():
#             raise serializers.ValidationError("Incorrect CAPTCHA.")

#         captcha.delete()  # Remove solved CAPTCHA

#         return data
    
#     def create(self, validated_data):
#         return Comment.objects.create(**validated_data)

from rest_framework import serializers
from .models import Comment
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


class CommentSerializer(serializers.ModelSerializer):
    captcha_key = serializers.CharField(write_only=True)
    captcha_value = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'name', 'email', 'homepage', 'text',
            'file', 'created_at',
            'captcha_key', 'captcha_value'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        # CAPTCHA validation
        captcha_key = data.get('captcha_key')
        captcha_value = data.get('captcha_value')

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError({'captcha_value': 'Invalid CAPTCHA key.'})

        if captcha.response != captcha_value.strip().lower():
            raise serializers.ValidationError({'captcha_value': 'Incorrect CAPTCHA.'})

        # Cleaned up after validation
        data.pop('captcha_key')
        data.pop('captcha_value')

        return data
