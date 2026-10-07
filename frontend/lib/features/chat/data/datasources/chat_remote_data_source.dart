import '../../../../core/network/api_client.dart';
import '../models/chat_reply_model.dart';

class ChatRemoteDataSource {
  const ChatRemoteDataSource(this._apiClient);

  final ApiClient _apiClient;

  Future<ChatReplyModel> sendMessage({
    required String message,
    required String profile,
  }) async {
    final response = await _apiClient.post(
      '/api/v1/chat',
      body: {'message': message, 'profile': profile},
    );
    return ChatReplyModel.fromJson(response);
  }
}
