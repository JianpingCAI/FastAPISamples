from pydantic import BaseModel

class BaseClass(BaseModel):
    name: str

class DerivedClass(BaseClass):
    id: str

    @classmethod
    def from_base(cls, base_instance: BaseClass, id: str):
        # Initialize the derived class using the base instance's data and the new id
        return cls(name=base_instance.name, id=id)

# Create an instance of BaseClass
base_instance = BaseClass(name="example_name")

# Create an instance of DerivedClass using the base_instance and an additional id
derived_instance = DerivedClass.from_base(base_instance, id="example_id")

# Output the derived_instance to demonstrate that initialization worked correctly
print(derived_instance.model_dump())
