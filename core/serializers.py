from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from core.models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField(required=False) # cut this - to focus this script on one responsibility

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']
        # extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']