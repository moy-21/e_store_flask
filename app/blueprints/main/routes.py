from .import bp as main
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Item, User, Cart
from .forms import ItemForm

# ROUTES
@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    form = ItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        item_data = {
            "name" :form.name.data,
            "desc" : form.desc.data,
            "price" : form.price.data,
            "img" :form.img.data
        }
        new_item = Item()
        new_item.from_dict(item_data)
        new_item.save()
        flash('You have successfully added you item', 'success')
        return redirect(url_for('main.post'))
    return render_template('post.html.j2', form=form)

@main.route('/add_item/<int:item_id>', methods = ['GET', 'POST'])
@login_required
def add_item(item_id):
    item = Item.query.get(item_id)
    current_user.add_to_cart(item)
    Cart(item_id=item_id, user_id = current_user.id )
    flash(f'You have added item to cart.', "success")
    return redirect(request.referrer or url_for('main.item', item= item))
       
@main.route('/remove_item/<int:item_id>', methods = ['GET', 'POST'])
@login_required
def remove_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    current_user.remove_item(item)
    flash(f'You have removed item from cart.', "success")
    return redirect(request.referrer or url_for('main.cart',item= item))

@main.route('/remove_all' , methods = ['GET', 'POST'])
@login_required
def remove_all():
    cart = current_user.cart
    current_user.remove_all(cart)
    flash(f'You have removed all items from cart.', "success")
    return redirect(request.referrer or url_for('main.cart',item= item))
 
  
@main.route('/cart', methods = ['GET', 'POST'])
@login_required
def cart():
    cart = current_user.cart
    
    return render_template('cart.html.j2',cart=cart)

@main.route('/shop', methods = ['GET', 'POST'])
def shop():
    items = Item.query.all()


    return render_template('main_store.html.j2',items = items)

@main.route('/get_item/<int:item_id>', methods = ['GET', 'POST'])
@login_required
def get_item(item_id):
    item = Item.query.get(item_id)

    return render_template('get_item.html.j2',item=item)

@main.route('/pay', methods = ['GET', 'POST'])
@login_required
def pay():
    total = []
    cart = current_user.cart
    for item in cart:
        price = item.price
        total.append(price)

    total = sum(total)


    return render_template('payment.html.j2',total=total)




