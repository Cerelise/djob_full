import os
import uuid

from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# from .forms import CompanyForm
from .permissions import IsEmployerOrReadOnly


@api_view(['POST'])
@permission_classes([IsEmployerOrReadOnly])
def uploadCompanyPhoto(request):

    picture = request.data
    keyword_list = list(picture.keys())
    keyword = keyword_list[0]
    
    if keyword == 'avatar':
        picture_path = handle_single_photo(picture['avatar'],keyword)
    elif keyword == 'main_photo':
        picture_path = handle_single_photo(picture['main_photo'],keyword)
    else:
        picture_path = handle_single_photo(picture['photo'],'photo')

    response = picture_path.replace('\\','/')

    return Response(response,status=status.HTTP_200_OK)


def handle_photo(file,company,photo_type):
    
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10],ext)
    if photo_type == 'avatar':
        handle_pic = os.path.join(company,"avatar",file_name)
        pic_path = os.path.join("media","company",company,"avatar",file_name)
    else:
        handle_pic = os.path.join(company,"album",file_name)
        pic_path = os.path.join("media","company",company,"album",file_name)
    
    os.makedirs(os.path.dirname(pic_path), exist_ok=True)

    img = Image.open(file)

    img.save(pic_path)

    return handle_pic


def handle_single_photo(file,photo_type):
    
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10],ext)
    if photo_type == 'avatar':
        # handle_pic = os.path.join("logo",file_name)
        pic_path = os.path.join("media","company","logo",file_name)
    elif photo_type == 'main_photo':
        # handle_pic = os.path.join("main",file_name)
        pic_path = os.path.join("media","company","main",file_name)
    elif photo_type == 'photo':
        # handle_pic = os.path.join("album",file_name)
        pic_path = os.path.join("media","company","album",file_name)
    
    os.makedirs(os.path.dirname(pic_path), exist_ok=True)

    img = Image.open(file)

    img.save(pic_path)

    return pic_path
