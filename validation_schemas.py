from marshmallow import Schema, fields, validate
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    id_user = fields.Integer(strict=True)
    username = fields.String(required=True, validate=Length(min=3,max=255))
    first_name = fields.String(required=True, validate=Length(min=3,max=255))
    last_name = fields.String(required=True, validate=Length(min=3,max=255))
    age = fields.Integer(required=True, strict=True)
    email = fields.String(required=True, validate=Length(min=12,max=255))
    password = fields.String(required=True, validate=Length(min=4,max=255))
    phone_number = fields.String(required=True, validate=Length(min=9,max=20))
    userstatus = fields.Str(required=True, validate=validate.OneOf(["user", "pharmacist"]))


class Order_detailsSchema(Schema):
    order_id = fields.Integer(required=True)
    medicine_id = fields.Integer(required=True)
    count = fields.Integer(required=True)


class MedicineSchema(Schema):
    id_medicine = fields.Integer(strict=True)
    medicine_name = fields.String(required=True, validate=Length(min=3,max=65))
    manufacturer = fields.String(required=True, validate=Length(min=3,max=65))
    medicine_description = fields.String(required=True, validate=Length(min=4,max=255))
    category_id = fields.Integer(required=True, strict=True)
    price = fields.Integer(required=True, strict=True)
    medicine_status = fields.Str(required=True, validate=validate.OneOf(["available", "pending", "sold"]))
    demand = fields.Boolean(required=True, strict=True)


class OrderSchema(Schema):
    id_order = fields.Integer(strict=True)
    user_id = fields.Integer(required=True, strict=True)
    address = fields.String(required=True, validate=Length(min=5,max=350))
    date_of_purchase = fields.DateTime(required=True)
    shipData = fields.DateTime(required=True)
    order_status = fields.Str(required=True, validate=validate.OneOf(["placed", "approved", "delivered"]))
    complete = fields.Boolean(required=True, strict=True)


class CategorySchema(Schema):
    id_category = fields.Integer(strict=True)
    category_name = fields.String(required=True, validate=Length(min=4,max=255))
    description = fields.String(required=True, validate=Length(min=4,max=300))


class UserSchemaUpdate(Schema):
    id_user = fields.Integer(strict=True)
    username = fields.String(validate=Length(min=3,max=255))
    first_name = fields.String(validate=Length(min=3,max=255))
    last_name = fields.String(validate=Length(min=3,max=255))
    age = fields.Integer(strict=True)
    email = fields.String(validate=Length(min=12,max=255))
    password = fields.String(validate=Length(min=4,max=255))
    phone_number = fields.String(validate=Length(min=9,max=20))
    userstatus = fields.Str(validate=validate.OneOf(["user", "pharmacist"]))


class Order_detailsSchemaUpdate(Schema):
    order_id = fields.Integer()
    medicine_id = fields.Integer()
    count = fields.Integer()


class MedicineSchemaUpdate(Schema):
    id_medicine = fields.Integer(strict=True)
    medicine_name = fields.String(validate=Length(min=3,max=65))
    manufacturer = fields.String(validate=Length(min=3,max=65))
    medicine_description = fields.String(validate=Length(min=4,max=255))
    category_id = fields.Integer(strict=True)
    price = fields.Integer(strict=True)
    medicine_status = fields.Str(validate=validate.OneOf(["available", "pending", "sold"]))
    demand = fields.Boolean(strict=True)


class OrderSchemaUpdate(Schema):
    id_order = fields.Integer(strict=True)
    user_id = fields.Integer(strict=True)
    address = fields.String(validate=Length(min=5,max=350))
    date_of_purchase = fields.DateTime()
    shipData = fields.DateTime()
    order_status = fields.Str(validate=validate.OneOf(["placed", "approved", "delivered"]))
    complete = fields.Boolean(strict=True)


class CategorySchemaUpdate(Schema):
    id_category = fields.Integer(strict=True)
    category_name = fields.String(validate=Length(min=4,max=255))
    description = fields.String(validate=Length(min=4,max=300))

