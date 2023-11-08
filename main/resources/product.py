from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductModel, RatingModel

class Product(Resource):
    def get(self,id):
        product = db.session.query(ProductModel).get_or_404(id)
        return product.to_json()
    
    def delete(self,id):
        product = db.session.query(ProductModel).get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return "", 204
        
    def put(self, id):
        product = db.session.query(ProductModel).get_or_404(id)
        if not product:
            return {'message': 'Producto no encontrado'}, 404
        
        data = request.get_json()
        if 'title' in data:
            product.titulo = data['title']
        if 'price' in data:
            product.precio_compra = data['price']
        if 'description' in data:
            product.descripcion = data['description']
        if 'category' in data:
            product.categoria = data['category']
        if 'image' in data:
            product.url_imagen = data['image']

        rating_data = data.get('rating')
        if rating_data:
            if product.rating:
                product.rating.rate = rating_data.get('rate')
                product.rating.count = rating_data.get('count')
            else:
                rating = RatingModel(
                    rate=rating_data.get('rate'),
                    count=rating_data.get('count')
                )
                product.rating = rating
        db.session.commit()
        return product.to_json(), 200

    

class Products(Resource):
    def get(self):
        products = db.session.query(ProductModel)

        precio_minimo = request.args.get('precioMinimo')

        if precio_minimo:
            try:
                precio_minimo = float(precio_minimo)
                products = products.filter(ProductModel.precio_compra >= precio_minimo)
            except Exception:
                return {"Error, por favor intente mas tarde."}, 400

        precio_maximo = request.args.get('precioMaximo')
        if precio_maximo:
            try:
                precio_maximo = float(precio_maximo)
                products = products.filter(ProductModel.precio_compra <= precio_maximo)
            except Exception:
                return {"Error, por favor intente mas tarde."}, 400

        products = products.all()

        return jsonify([product.to_json() for product in products])





    def post(self):
        data = request.get_json()
        product_data = {
            "titulo": data.get('title'),
            "precio_compra": data.get('price'),
            "descripcion": data.get('description'),
            "categoria": data.get('category'),
            "url_imagen": data.get('image'),
        }
        product = ProductModel.from_json(product_data)
        rating_data = data.get('rating')
        if rating_data:
            rating = RatingModel(
                rate=rating_data.get('rate'),
                count=rating_data.get('count')
            )
            product.rating = rating
            db.session.add(rating)
        db.session.add(product)
        db.session.commit()
        return product.to_json(), 201
    
