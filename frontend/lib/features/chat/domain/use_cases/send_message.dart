import '../repositories/chat_repository.dart';

class SendMessage {
  const SendMessage(this._repository);

  final ChatRepository _repository;

  Future<ChatReply> call({
    required String message,
    required String profile,
  }) {
    return _repository.sendMessage(message: message, profile: profile);
  }
}
