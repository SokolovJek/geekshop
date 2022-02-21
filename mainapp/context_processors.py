from basketapp.models import BasketModel


def basket(request):
   print(f'context processor basket works')
   basket = []

   if request.user.is_authenticated:
       basket = BasketModel.objects.filter(user=request.user).select_related()

   return {
       'basket': basket,
   }