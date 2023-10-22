import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import attr
from pytest import importorskip

from omegaconf import II, MISSING, SI
from tests import Color, Enum1

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import TypedDict

# attr is a dependency of pytest which means it's always available when testing with pytest.
importorskip("attr")


class NotStructuredConfig:
    name: str = "Bond"
    age: int = 7

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, type(self)):
            return self.name == other.name and self.age == other.age
        return False


if sys.version_info >= (3, 8):  # pragma: no cover

    class TypedDictSubclass(TypedDict):
        foo: int


@attr.s(auto_attribs=True)
class StructuredWithInvalidField:
    bar: NotStructuredConfig = attr.Factory(NotStructuredConfig)


@attr.s(auto_attribs=True)
class User:
    name: str = MISSING
    age: int = MISSING


@attr.s(auto_attribs=True)
class UserList:
    list: List[User] = MISSING


@attr.s(auto_attribs=True)
class UserDict:
    dict: Dict[str, User] = MISSING


@attr.s(auto_attribs=True)
class UserWithDefaultName(User):
    name: str = "bob"


@attr.s(auto_attribs=True)
class MissingUserField:
    user: User = MISSING


@attr.s(auto_attribs=True)
class MissingUserWithDefaultNameField:
    user: UserWithDefaultName = MISSING


@attr.s(auto_attribs=True)
class OptionalUser:
    user: Optional[User] = None


@attr.s(auto_attribs=True)
class InterpolationToUser:
    user: User = attr.Factory(lambda: User("Bond", 7))
    admin: User = II("user")


@attr.s(auto_attribs=True)
class AnyTypeConfig:
    with_default: Any = "Can get any type at runtime"
    null_default: Any = None
    # Access to this prior to assigning a value to it will result in
    # a MissingMandatoryValue exception.
    # Equivalent to "???" in YAML files
    mandatory_missing: Any = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: Any = II("with_default")

    # specific types assigned
    int_default: Any = 12
    float_default: Any = 10.0
    str_default: Any = "foobar"
    bool_default: Any = True
    enum_default: Any = Color.BLUE

    # test mixing with variable with a specific type annotation
    typed_int_default: int = 10


@attr.s(auto_attribs=True)
class BoolConfig:
    # with default value
    with_default: bool = True

    # default is None
    null_default: Optional[bool] = None

    # explicit no default
    mandatory_missing: bool = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: bool = II("with_default")


@attr.s(auto_attribs=True)
class IntegersConfig:
    # with default value
    with_default: int = 10

    # default is None
    null_default: Optional[int] = None

    # explicit no default
    mandatory_missing: int = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: int = II("with_default")


@attr.s(auto_attribs=True)
class StringConfig:
    # with default value
    with_default: str = "foo"

    # default is None
    null_default: Optional[str] = None

    # explicit no default
    mandatory_missing: str = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: str = II("with_default")


@attr.s(auto_attribs=True)
class FloatConfig:
    # with default value
    with_default: float = 0.10

    # default is None
    null_default: Optional[float] = None

    # explicit no default
    mandatory_missing: float = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: float = II("with_default")


@attr.s(auto_attribs=True)
class BytesConfig:
    # with default value
    with_default: bytes = b"binary"

    # default is None
    null_default: Optional[bytes] = None

    # explicit no default
    mandatory_missing: bytes = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: bytes = II("with_default")


@attr.s(auto_attribs=True)
class PathConfig:
    # with default value
    with_default: Path = Path("hello.txt")

    # default is None
    null_default: Optional[Path] = None

    # explicit no default
    mandatory_missing: Path = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: Path = II("with_default")


@attr.s(auto_attribs=True)
class EnumConfig:
    # with default value
    with_default: Color = Color.BLUE

    # default is None
    null_default: Optional[Color] = None

    # explicit no default
    mandatory_missing: Color = MISSING

    # interpolation, will inherit the type and value of `with_default'
    interpolation: Color = II("with_default")


@attr.s(auto_attribs=True)
class ConfigWithList:
    list1: List[int] = attr.Factory(lambda: [1, 2, 3])
    list2: Tuple[int, int, int] = attr.Factory(lambda: (1, 2, 3))
    missing: List[int] = MISSING


@attr.s(auto_attribs=True)
class ConfigWithDict:
    dict1: Dict[str, Any] = attr.Factory(lambda: {"foo": "bar"})
    missing: Dict[str, Any] = MISSING


@attr.s(auto_attribs=True)
class ConfigWithDict2:
    dict1: Dict[str, int] = attr.Factory(lambda: {"foo": 2})


@attr.s(auto_attribs=True)
class Nested:
    # with default value
    with_default: int = 10

    # default is None
    null_default: Optional[int] = None

    # explicit no default
    mandatory_missing: int = MISSING

    # Note that since relative interpolations are not yet supported,
    # Nested configs and interpolations does not play too well together
    interpolation: int = II("value_at_root")


@attr.s(auto_attribs=True)
class NestedSubclass(Nested):
    additional: int = 20


@attr.s(auto_attribs=True)
class NestedConfig:
    default_value: Nested

    # with default value
    user_provided_default: Nested = attr.Factory(lambda: Nested(with_default=42))

    value_at_root: int = 1000


@attr.s(auto_attribs=True)
class NestedWithAny:
    var: Any = attr.Factory(lambda: Nested())


@attr.s(auto_attribs=True)
class NoDefaultValue:
    no_default: Any


@attr.s(auto_attribs=True)
class Interpolation:
    x: int = 100
    y: int = 200
    # The real type of y is int, cast the interpolation string
    # to help static type checkers to see this truth
    z1: int = II("x")
    z2: str = SI("${x}_${y}")


@attr.s(auto_attribs=True)
class RelativeInterpolation:
    x: int = 100
    y: int = 200
    z1: int = II(".x")
    z2: str = SI("${.x}_${.y}")


@attr.s(auto_attribs=True)
class BoolOptional:
    with_default: Optional[bool] = True
    as_none: Optional[bool] = None
    not_optional: bool = True


@attr.s(auto_attribs=True)
class IntegerOptional:
    with_default: Optional[int] = 1
    as_none: Optional[int] = None
    not_optional: int = 1


@attr.s(auto_attribs=True)
class FloatOptional:
    with_default: Optional[float] = 1.0
    as_none: Optional[float] = None
    not_optional: float = 1


@attr.s(auto_attribs=True)
class StringOptional:
    with_default: Optional[str] = "foo"
    as_none: Optional[str] = None
    not_optional: str = "foo"


@attr.s(auto_attribs=True)
class ListOptional:
    with_default: Optional[List[int]] = attr.Factory(lambda: [1, 2, 3])
    as_none: Optional[List[int]] = None
    not_optional: List[int] = attr.Factory(lambda: [1, 2, 3])


@attr.s(auto_attribs=True)
class TupleOptional:
    with_default: Optional[Tuple[int, int, int]] = attr.Factory(lambda: (1, 2, 3))
    as_none: Optional[Tuple[int, int, int]] = None
    not_optional: Tuple[int, int, int] = attr.Factory(lambda: (1, 2, 3))


@attr.s(auto_attribs=True)
class EnumOptional:
    with_default: Optional[Color] = Color.BLUE
    as_none: Optional[Color] = None
    not_optional: Color = Color.BLUE


@attr.s(auto_attribs=True)
class DictOptional:
    with_default: Optional[Dict[str, int]] = attr.Factory(lambda: {"a": 10})
    as_none: Optional[Dict[str, int]] = None
    not_optional: Dict[str, int] = attr.Factory(lambda: {"a": 10})


@attr.s(auto_attribs=True)
class RecursiveDict:
    d: Dict[str, "RecursiveDict"] = MISSING


@attr.s(auto_attribs=True)
class StructuredOptional:
    with_default: Optional[Nested] = attr.Factory(Nested)
    as_none: Optional[Nested] = None
    not_optional: Nested = attr.Factory(Nested)


@attr.s(auto_attribs=True, frozen=True)
class FrozenClass:
    user: User = attr.Factory(lambda: User(name="Bart", age=10))
    x: int = 10
    list: List[int] = attr.Factory(lambda: [1, 2, 3])


@attr.s(auto_attribs=True)
class ContainsFrozen:
    x: int = 10
    frozen: FrozenClass = FrozenClass()


@attr.s(auto_attribs=True)
class WithListField:
    list: List[int] = attr.Factory(lambda: [1, 2, 3])


@attr.s(auto_attribs=True)
class WithDictField:
    dict: Dict[str, int] = attr.Factory(lambda: {"foo": 10, "bar": 20})


if sys.version_info >= (3, 8):  # pragma: no cover

    @attr.s(auto_attribs=True)
    class WithTypedDictField:
        dict: TypedDictSubclass


@attr.s(auto_attribs=True)
class ErrorDictObjectKey:
    # invalid dict key, must be str
    dict: Dict[object, str] = attr.Factory(lambda: {object(): "foo", object(): "bar"})


class RegularClass:
    pass


@attr.s(auto_attribs=True)
class ErrorDictUnsupportedValue:
    # invalid dict value type, not one of the supported types
    dict: Dict[str, RegularClass] = attr.Factory(dict)


@attr.s(auto_attribs=True)
class ErrorListUnsupportedValue:
    # invalid dict value type, not one of the supported types
    dict: List[RegularClass] = attr.Factory(list)


@attr.s(auto_attribs=True)
class ListExamples:
    any: List[Any] = attr.Factory(lambda: [1, "foo"])
    ints: List[int] = attr.Factory(lambda: [1, 2])
    strings: List[str] = attr.Factory(lambda: ["foo", "bar"])
    booleans: List[bool] = attr.Factory(lambda: [True, False])
    colors: List[Color] = attr.Factory(lambda: [Color.RED, Color.GREEN])


@attr.s(auto_attribs=True)
class TupleExamples:
    any: Tuple[Any, Any] = attr.Factory(lambda: (1, "foo"))
    ints: Tuple[int, int] = attr.Factory(lambda: (1, 2))
    strings: Tuple[str, str] = attr.Factory(lambda: ("foo", "bar"))
    booleans: Tuple[bool, bool] = attr.Factory(lambda: (True, False))
    colors: Tuple[Color, Color] = attr.Factory(lambda: (Color.RED, Color.GREEN))


@attr.s(auto_attribs=True)
class DictExamples:
    any: Dict[str, Any] = attr.Factory(lambda: {"a": 1, "b": "foo"})
    ints: Dict[str, int] = attr.Factory(lambda: {"a": 10, "b": 20})
    strings: Dict[str, str] = attr.Factory(lambda: {"a": "foo", "b": "bar"})
    booleans: Dict[str, bool] = attr.Factory(lambda: {"a": True, "b": False})
    colors: Dict[str, Color] = attr.Factory(
        lambda: {
            "red": Color.RED,
            "green": Color.GREEN,
            "blue": Color.BLUE,
        }
    )
    int_keys: Dict[int, str] = attr.Factory(lambda: {1: "one", 2: "two"})
    float_keys: Dict[float, str] = attr.Factory(lambda: {1.1: "one", 2.2: "two"})
    bool_keys: Dict[bool, str] = attr.Factory(lambda: {True: "T", False: "F"})
    enum_key: Dict[Color, str] = attr.Factory(
        lambda: {Color.RED: "red", Color.GREEN: "green"}
    )


@attr.s(auto_attribs=True)
class DictOfObjects:
    users: Dict[str, User] = attr.Factory(lambda: {"joe": User(name="Joe", age=18)})


@attr.s(auto_attribs=True)
class DictOfObjectsMissing:
    users: Dict[str, User] = attr.Factory(lambda: {"moe": MISSING})


@attr.s(auto_attribs=True)
class ListOfObjects:
    users: List[User] = attr.Factory(lambda: [User(name="Joe", age=18)])


@attr.s(auto_attribs=True)
class ListOfObjectsMissing:
    users: List[User] = attr.Factory(lambda: [MISSING])


class DictSubclass:
    @attr.s(auto_attribs=True)
    class Str2Str(Dict[str, str]):
        pass

    @attr.s(auto_attribs=True)
    class Str2Int(Dict[str, int]):
        pass

    @attr.s(auto_attribs=True)
    class Int2Str(Dict[int, str]):
        pass

    @attr.s(auto_attribs=True)
    class Float2Str(Dict[float, str]):
        pass

    @attr.s(auto_attribs=True)
    class Bool2Str(Dict[bool, str]):
        pass

    @attr.s(auto_attribs=True)
    class Color2Str(Dict[Color, str]):
        pass

    @attr.s(auto_attribs=True)
    class Color2Color(Dict[Color, Color]):
        pass

    @attr.s(auto_attribs=True)
    class Str2User(Dict[str, User]):
        pass

    @attr.s(auto_attribs=True)
    class Str2StrWithField(Dict[str, str]):
        foo: str = "bar"

    @attr.s(auto_attribs=True)
    class Str2IntWithStrField(Dict[str, int]):
        foo: int = 1

    @attr.s(auto_attribs=True)
    class Str2UserWithField(Dict[str, User]):
        foo: User = attr.Factory(lambda: User("Bond", 7))

    class Error:
        @attr.s(auto_attribs=True)
        class User2Str(Dict[User, str]):
            pass


@attr.s(auto_attribs=True)
class Plugin:
    name: str = MISSING
    params: Any = MISSING


@attr.s(auto_attribs=True)
class ConcretePlugin(Plugin):
    name: str = "foobar_plugin"

    @attr.s(auto_attribs=True)
    class FoobarParams:
        foo: int = 10

    params: FoobarParams = attr.Factory(FoobarParams)


@attr.s(auto_attribs=True)
class PluginWithAdditionalField(Plugin):
    name: str = "foobar2_plugin"
    additional: int = 10


# Does not extend Plugin, cannot be assigned or merged
@attr.s(auto_attribs=True)
class FaultyPlugin:
    name: str = "faulty_plugin"


@attr.s(auto_attribs=True)
class PluginHolder:
    none: Optional[Plugin] = None
    missing: Plugin = MISSING
    plugin: Plugin = attr.Factory(Plugin)
    plugin2: Plugin = attr.Factory(ConcretePlugin)


@attr.s(auto_attribs=True)
class LinkedList:
    next: Optional["LinkedList"] = None
    value: Any = MISSING


@attr.s(auto_attribs=True)
class RecursiveList:
    d: List["RecursiveList"] = MISSING


class MissingTest:
    @attr.s(auto_attribs=True)
    class Missing1:
        head: LinkedList = MISSING

    @attr.s(auto_attribs=True)
    class Missing2:
        head: LinkedList = attr.Factory(lambda: LinkedList(next=MISSING, value=1))


@attr.s(auto_attribs=True)
class NestedWithNone:
    plugin: Optional[Plugin] = None


@attr.s(auto_attribs=True)
class UnionError:
    x: Union[int, List[str]] = 10


@attr.s(auto_attribs=True)
class WithNativeMISSING:
    num: int = attr.NOTHING  # type: ignore


@attr.s(auto_attribs=True)
class MissingStructuredConfigField:
    plugin: Plugin = MISSING


@attr.s(auto_attribs=True)
class ListClass:
    list: List[int] = attr.Factory(lambda: [])
    tuple: Tuple[int, int] = attr.Factory(lambda: (1, 2))


@attr.s(auto_attribs=True)
class UntypedList:
    list: List = attr.Factory(lambda: [1, 2])  # type: ignore
    opt_list: Optional[List] = None  # type: ignore


@attr.s(auto_attribs=True)
class UntypedDict:
    dict: Dict = attr.Factory(lambda: {"foo": "var"})  # type: ignore
    opt_dict: Optional[Dict] = None  # type: ignore


class StructuredSubclass:
    @attr.s(auto_attribs=True)
    class ParentInts:
        int1: int
        int2: int
        int3: int = attr.NOTHING  # type: ignore
        int4: int = MISSING

    @attr.s(auto_attribs=True)
    class ChildInts(ParentInts):
        int2: int = 5
        int3: int = 10
        int4: int = 15

    @attr.s(auto_attribs=True)
    class ParentContainers:
        list1: List[int] = MISSING
        list2: List[int] = attr.Factory(lambda: [5, 6])
        dict: Dict[str, Any] = MISSING

    @attr.s(auto_attribs=True)
    class ChildContainers(ParentContainers):
        list1: List[int] = attr.Factory(lambda: [1, 2, 3])
        dict: Dict[str, Any] = attr.Factory(lambda: {"a": 5, "b": 6})

    @attr.s(auto_attribs=True)
    class ParentNoDefaultFactory:
        no_default_to_list: Any
        int_to_list: Any = 1

    @attr.s(auto_attribs=True)
    class ChildWithDefaultFactory(ParentNoDefaultFactory):
        no_default_to_list: Any = attr.Factory(lambda: ["hi"])
        int_to_list: Any = attr.Factory(lambda: ["hi"])


@attr.s(auto_attribs=True)
class HasInitFalseFields:
    post_initialized: str = attr.field(init=False)
    without_default: str = attr.field(init=False)
    with_default: str = attr.field(init=False, default="default")

    def __attrs_post_init__(self) -> None:
        self.post_initialized = "set_by_post_init"


class NestedContainers:
    @attr.s(auto_attribs=True)
    class ListOfLists:
        lls: List[List[str]]
        llx: List[List[User]]
        llla: List[List[List[Any]]]
        lloli: List[List[Optional[List[int]]]]
        lls_default: List[List[str]] = attr.Factory(
            lambda: [[], ["abc", "def", 123, MISSING], MISSING]  # type: ignore
        )
        lolx_default: List[Optional[List[User]]] = attr.Factory(
            lambda: [
                [],
                [User(), User(age=7, name="Bond"), MISSING],
                MISSING,
            ]
        )

    @attr.s(auto_attribs=True)
    class DictOfDicts:
        dsdsi: Dict[str, Dict[str, int]]
        dsdbi: Dict[str, Dict[bool, int]]
        dsdsx: Dict[str, Dict[str, User]]
        odsdsi_default: Optional[Dict[str, Dict[str, int]]] = attr.Factory(
            lambda: {
                "dsi1": {},
                "dsi2": {"s1": 1, "s2": "123", "s3": MISSING},
                "dsi3": MISSING,
            }
        )
        dsdsx_default: Dict[str, Dict[str, User]] = attr.Factory(
            lambda: {
                "dsx1": {},
                "dsx2": {
                    "s1": User(),
                    "s2": User(age=7, name="Bond"),
                    "s3": MISSING,
                },
                "dsx3": MISSING,
            }
        )

    @attr.s(auto_attribs=True)
    class ListsAndDicts:
        lldsi: List[List[Dict[str, int]]]
        ldaos: List[Dict[Any, Optional[str]]]
        dedsle: Dict[Color, Dict[str, List[Enum1]]]
        dsolx: Dict[str, Optional[List[User]]]
        oldfox: Optional[List[Dict[float, Optional[User]]]]
        dedsle_default: Dict[Color, Dict[str, List[Enum1]]] = attr.Factory(
            lambda: {
                Color.RED: {"a": [Enum1.FOO, Enum1.BAR]},
                Color.GREEN: {"b": []},
                Color.BLUE: {},
            }
        )

    @attr.s(auto_attribs=True)
    class WithDefault:
        dsolx_default: Dict[str, Optional[List[User]]] = attr.Factory(
            lambda: {"lx": [User()], "n": None}
        )


class UnionsOfPrimitveTypes:
    @attr.s(auto_attribs=True)
    class Simple:
        uis: Union[int, str]
        ubc: Union[bool, Color]
        uxf: Union[bytes, float]
        ouis: Optional[Union[int, str]]
        uois: Union[Optional[int], str]
        uisn: Union[int, str, None]
        uisN: Union[int, str, type(None)]  # type: ignore

    @attr.s(auto_attribs=True)
    class WithDefaults:
        uis: Union[int, str] = "abc"
        ubc1: Union[bool, Color] = True
        ubc2: Union[bool, Color] = Color.RED
        uxf: Union[bytes, float] = 1.2
        ouis: Optional[Union[int, str]] = None
        uisn: Union[int, str, None] = 123
        uisN: Union[int, str, type(None)] = "abc"  # type: ignore

    @attr.s(auto_attribs=True)
    class WithExplicitMissing:
        uis_missing: Union[int, str] = MISSING

    @attr.s(auto_attribs=True)
    class WithBadDefaults1:
        uis: Union[int, str] = None  # type: ignore

    @attr.s(auto_attribs=True)
    class WithBadDefaults2:
        ubc: Union[bool, Color] = "abc"  # type: ignore

    @attr.s(auto_attribs=True)
    class WithBadDefaults3:
        uxf: Union[bytes, float] = True

    @attr.s(auto_attribs=True)
    class WithBadDefaults4:
        oufb: Optional[Union[float, bool]] = Color.RED  # type: ignore

    @attr.s(auto_attribs=True)
    class ContainersOfUnions:
        lubc: List[Union[bool, Color]]
        dsubf: Dict[str, Union[bool, float]]
        dsoubf: Dict[str, Optional[Union[bool, float]]]
        lubc_with_default: List[Union[bool, Color]] = attr.Factory(
            lambda: [True, Color.RED]
        )
        dsubf_with_default: Dict[str, Union[bool, float]] = attr.Factory(
            lambda: {"abc": True, "xyz": 1.2}
        )

    @attr.s(auto_attribs=True)
    class InterpolationFromUnion:
        ubi: Union[bool, int]
        oubi: Optional[Union[bool, int]]
        an_int: int = 123
        a_string: str = "abc"
        missing: int = MISSING
        none: Optional[int] = None
        ubi_with_default: Union[bool, int] = II("an_int")
        oubi_with_default: Optional[Union[bool, int]] = II("none")

    @attr.s(auto_attribs=True)
    class InterpolationToUnion:
        a_float: float = II("ufs")
        bad_int_interp: bool = II("ufs")
        ufs: Union[float, str] = 10.1

    @attr.s(auto_attribs=True)
    class BadInterpolationFromUnion:
        a_float: float = 10.1
        ubi: Union[bool, int] = II("a_float")

    if sys.version_info >= (3, 10):

        @attr.s(auto_attribs=True)
        class SupportPEP604:
            """https://peps.python.org/pep-0604/"""

            uis: int | str
            ouis: Optional[int | str]
            uisn: int | str | None = None
            uis_with_default: int | str = 123


if sys.version_info >= (3, 9):

    @attr.s(auto_attribs=True)
    class SupportPEP585:
        """
        PEP 585 – Type Hinting Generics In Standard Collections
        https://peps.python.org/pep-0585/

        This means lower-case dict/list/tuple annotations
        can be used instad of uppercase Dict/List/Tuple.
        """

        dict_: dict[int, str] = attr.Factory(lambda: {123: "abc"})
        list_: list[int] = attr.Factory(lambda: [123])
        tuple_: tuple[int] = (123,)
        dict_no_subscript: dict = attr.Factory(lambda: {123: "abc"})
        list_no_subscript: list = attr.Factory(lambda: [123])
        tuple_no_subscript: tuple = (123,)


@attr.s(auto_attribs=True)
class HasForwardRef:
    @attr.s(auto_attribs=True)
    class CA:
        x: int = 3

    @attr.s(auto_attribs=True)
    class CB:
        sub: "HasForwardRef.CA"

    a: CA
    b: CB


@attr.s(auto_attribs=True)
class HasBadAnnotation1:
    data: object


@attr.s(auto_attribs=True)
class HasBadAnnotation2:
    data: object()  # type: ignore


@attr.s(auto_attribs=True)
class HasIgnoreMetadataRequired:
    ignore: int = attr.field(metadata={"omegaconf_ignore": True})
    no_ignore: int = attr.field(metadata={"omegaconf_ignore": False})


@attr.s(auto_attribs=True)
class HasIgnoreMetadataWithDefault:
    ignore: int = attr.field(default=1, metadata={"omegaconf_ignore": True})
    no_ignore: int = attr.field(default=2, metadata={"omegaconf_ignore": False})
