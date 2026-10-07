import '../../domain/repositories/chat_repository.dart';
import '../datasources/chat_remote_data_source.dart';

class ChatRepositoryImpl implements ChatRepository {
  const ChatRepositoryImpl(this._remoteDataSource);

  final ChatRemoteDataSource _remoteDataSource;

  @override
  Future<ChatReply> sendMessage({
    required String message,
    required String profile,
  }) {
    return _remoteDataSource.sendMessage(message: message, profile: profile);
  }
}
