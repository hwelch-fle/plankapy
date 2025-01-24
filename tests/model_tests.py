import plankapy.models as models

from dataclasses import dataclass

def test_base_model():

    @dataclass(eq=False)
    class TestModel(models.Model):
        id: int=models.Unset
        name: str=models.Unset
        _private: str=models.Unset

    try:
        instance = TestModel(id=1, name='test', _private='private')
        assert 'private' not in instance, "Private attributes should not be included in __iter__"

        instance.name = models.Unset
        assert 'name' in instance, "Unset value should be skipped bt __iter__"

        instance2 = TestModel(**instance)

        assert 'private' not in instance2, "Private attributes should not be unpacked"
        assert hash(instance) == instance.id, "Hash should be equal to id"
        assert instance == instance2, "instances with same `id` should be equal"
    
    except AssertionError as e:
        print("Base Model Tests - Failed")
        return False
    
    print("Base Model Tests - Passed")
    return True