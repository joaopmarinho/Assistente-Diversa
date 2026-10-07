import '../../domain/entities/article_source.dart';
import '../../domain/repositories/chat_repository.dart';

class ChatReplyModel extends ChatReply {
  const ChatReplyModel({required super.answer, required super.sources});

  factory ChatReplyModel.fromJson(Map<String, dynamic> json) {
    final sources = (json['sources'] as List<dynamic>)
        .map((item) {
          final source = item as Map<String, dynamic>;
          return ArticleSource(
            id: source['id'] as String,
            title: source['title'] as String,
            summary: source['summary'] as String,
            sourceUrl: source['source_url'] as String,
          );
        })
        .toList(growable: false);
    return ChatReplyModel(
      answer: json['answer'] as String,
      sources: sources,
    );
  }
}
