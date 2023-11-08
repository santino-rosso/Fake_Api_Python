from .. import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255),nullable=False)
    precio_compra = db.Column(db.Numeric(precision=10,scale=2),nullable=False)
    descripcion = db.Column(db.String(255))
    categoria = db.Column(db.String(255))
    url_imagen = db. Column(db.String(255))

    rating = db.relationship('Rating', uselist=False, back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Product: %r %r %r %r %r>'% (self.titulo, self.precio_compra, self.descripcion, self.categoria, self.url_imagen)
    

    def to_json(self):
        product_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'precio_compra': str(self.precio_compra),
            'descripcion': str(self.descripcion),
            'categoria': str(self.categoria),
            'url_imagen': str(self.url_imagen),

        }
        return product_json


    @staticmethod
    def from_json(product_json):
        id = product_json.get('id')
        titulo = product_json.get('titulo')
        precio_compra = product_json.get('precio_compra')
        descripcion = product_json.get('descripcion')
        categoria = product_json.get('categoria')
        url_imagen = product_json.get('url_imagen')
        return Product(id=id,
                    titulo=titulo,
                    precio_compra=precio_compra,
                    descripcion=descripcion,
                    categoria=categoria,
                    url_imagen=url_imagen
                    )