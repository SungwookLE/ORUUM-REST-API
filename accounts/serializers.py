#  file: accounts/serializers.py

from rest_framework import serializers
from accounts.models import UserList, UserInterest, UserPortfolio, UserWallet


class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserList
        fields = ['id', 'email', 'username', 'thumbnail_image']


class UserInterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class UserPortfolioSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = '__all__'


class UserInformationSerializers(serializers.ModelSerializer): # (11/9) RetrieveAPIView에 serializer_class 없는 경우 에러 해결을 위한 임시방편으로 구성 
    class Meta:
        model = UserWallet
        fields = '__all__'


'''(11/22)
https://hayeon1549.tistory.com/36
class UserJWTSignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        write_only=True,
    )

    email = serializers.EmailField(
        required=True,
        write_only=True,
    )

    username = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    class Meta(object):
        model = UserList
        fields = ['id', 'email', 'username']

    def save(self, request):
        user = super().save()

        user.id = self.validated_data['id']
        user.email = self.validated_data['email']
        user.username = self.validated_data['username']

        user.save()

        return user

    def validate(self, data):
        id = data.get('id', None)

        if UserList.objects.filter(id=id).exists():
            raise serializers.ValidationError("user already exists")

        return data

class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({
                'user': {'username': user.username, 'email': user.email, 'id': user.id}, #(11/21) 고쳐야겠음..
                'access': access,
                'refresh': refresh
            })
            
'''