db = new Mongo().getDB("carrinho");
db.createCollection('clientes', { capped: false });
db.clientes.createIndex( {'email':1}, {unique: true})