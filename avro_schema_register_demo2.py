from schema_registry.client import SchemaRegistryClient, schema

client = SchemaRegistryClient(url="http://127.0.0.1:8081")

deployment_schema = {
    "namespace": "confluent.io.examples.serialization.avro",
    "type": "record",
    "name": "Image",
    "fields": [
        {
            "name": "img_base64",
            "type": "string"
        },
        {
            "name": "img_ht",
            "type": "int"
        },
        {
            "name": "img_wd",
            "type": "int"
        },
        {
            "name": "channel",
            "type": "int"
        },
        {
            "name": "frame_name",
            "type": "string"
        }
    ]
}

'''
{
"namespace": "confluent.io.examples.serialization.avro",
    "name": "User",
    "type": "record",
    "fields": [
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "favorite_number",
            "type": "long"
        },
        {
            "name": "favorite_color",
            "type": "string"
        }
    ]
}
'''
'''
{
    "type": "record",
    "namespace": "com.kubertenes",
    "name": "AvroDeployment",
    "fields": [
        {"name": "image", "type": "string"},
        {"name": "replicas", "type": "int"},
        {"name": "port", "type": "int"},
    ],
}
'''
avro_schema = schema.AvroSchema(deployment_schema)

schema_id = client.register("test-deployment", avro_schema)
