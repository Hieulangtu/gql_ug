import strawberry
import asyncio
from typing import List, Annotated, Optional
from uoishelpers.resolvers import createInputs

from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphResolvers import resolve_id
from ._GraphPermissions import (
    RoleBasedPermission, 
    OnlyForAuthentized,
    RBACPermission
)
from src.Dataloaders import (
    getLoadersFromInfo,
    getUserFromInfo)
from src.DBResolvers import DBResolvers

RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".roleTypeGQLModel")]

class RoleTypeListGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RoleTypeListModel
    
    pass

async def resolve_role_type_list_by_id(
    self, info: strawberry.types.Info, list_id: IDType
) -> List["RoleTypeGQLModel"]:
    # print("resolve_role_type_list_by_id", list_id)
    loader = RoleTypeListGQLModel.getLoader(info)
    roles = await loader.filter_by(list_id=list_id)
    # print("resolve_role_type_list_by_id", list_id)
    return roles  

@strawberry.field(
    description="""returns the list of roles types associated to id""",
    permission_classes=[OnlyForAuthentized])
async def role_type_list_by_id(
    self, info: strawberry.types.Info, list_id: IDType
) -> List["RoleTypeGQLModel"]:
    roles = await resolve_role_type_list_by_id(self, info, list_id)
    return roles

import asyncio
@strawberry.type(description="")
class RoleTypeListResult:
    id: IDType = None
    msg: str = None

    @strawberry.field(
        description="""Result of user operation""",
        permission_classes=[OnlyForAuthentized])
    async def role_types(self, info: strawberry.types.Info) -> List["RoleTypeGQLModel"]:
        from .roleTypeGQLModel import RoleTypeGQLModel
        
        rows = await resolve_role_type_list_by_id(self, info, list_id=self.id)
        result = (RoleTypeGQLModel.resolve_reference(info=info, id=r.type_id) for r in rows)
        
        return await asyncio.gather(*result)

import dataclasses
@dataclasses.dataclass
class RoleTypeInsertIntoList:
    type_id: IDType = None
    list_id: IDType = None
    createdby: strawberry.Private[IDType] = None

# class InsertMembershipPermission(RBACPermission):
#     message = "User is not allowed create new membership"
#     async def has_permission(self, source, info: strawberry.types.Info, membership: "MembershipInsertGQLModel") -> bool:
#         adminRoleNames = ["administrátor"]
#         allowedRoleNames = ["garant"]
#         role = await self.resolveUserRole(info, 
#             rbacobject=membership.group_id, 
#             adminRoleNames=adminRoleNames, 
#             allowedRoleNames=allowedRoleNames)
        
#         if not role: return False
#         return True

@strawberry.field(
    description="""adds to a list of role types new item""",
    permission_classes=[OnlyForAuthentized])
async def role_type_list_add(
    self, info: strawberry.types.Info, role_type_list_id: IDType, role_type_id: IDType
) -> "RoleTypeListResult":
    
    loader = RoleTypeListGQLModel.getLoader(info)
    roles = await loader.filter_by(list_id=role_type_list_id)
    roles = [*roles]
    
    isIn = next(filter(lambda row: row.type_id == role_type_id, roles), None)
    
    result = RoleTypeListResult(id=role_type_list_id, msg="ok")
    # result.msg = "fail" if isIn is None else "ok"
    if isIn:
        result.msg = "fail"
    else:
        whatToInsert = RoleTypeInsertIntoList(type_id=role_type_id, list_id=role_type_list_id)
        user = getUserFromInfo(info)
        whatToInsert.createdby = user["id"]
            
        row = await loader.insert(whatToInsert)
        if row is None:
            result.msg = "fail"
    return result

@dataclasses.dataclass
class RoleTypeDeleteFormList:
    id: IDType = None

@strawberry.field(
    description="""Finds an user by their id""",
    permission_classes=[OnlyForAuthentized])
async def role_type_list_remove(
    self, info: strawberry.types.Info, role_type_list_id: IDType, role_type_id: IDType
) -> List["RoleTypeListResult"]:
   
    loader = RoleTypeListGQLModel.getLoader(info)
    roles = loader.filter_by(list_id=id)
    roles = [*roles]
    isIn = next(filter(lambda row: (row.type_id == role_type_id), roles), None)
    result = RoleTypeListResult(id=role_type_list_by_id, msg="ok")
    result.msg = "fail" if isIn is None else "ok"
    if isIn:
        row = await loader.delete(isIn)
    return result