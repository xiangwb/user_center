# from user.models import User
# class Greeter(user_pb2_grpc.UserServicer):
#     def GetUserByID(self, request, context):
#         # TODO:需要考虑异常情况
#         user_id=request.user_id
#         user=User.objects.get(id=user_id)
#     return user_pb2.GetUserReply(user_id=user.id,
#                                  username=user.username,
#                                  graduated_school=user.graduated_school,
#                                  company=user.company,
#                                  title=user.title,
#                                  brief=user.brief
#                                  )
#
