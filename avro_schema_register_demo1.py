from schema_registry.client import SchemaRegistryClient, schema

client = SchemaRegistryClient(url="http://127.0.0.1:8081")

deployment_schema = {
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
avro_schema = schema.AvroSchema(deployment_schema)

schema_id = client.register("test-deployment", avro_schema)
