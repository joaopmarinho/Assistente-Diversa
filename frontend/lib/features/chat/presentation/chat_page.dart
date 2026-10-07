import 'package:flutter/material.dart';

import '../domain/entities/chat_message.dart';
import 'chat_controller.dart';

class ChatPage extends StatefulWidget {
  const ChatPage({required this.controller, super.key});

  final ChatController controller;

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final _messageController = TextEditingController();

  @override
  void dispose() {
    _messageController.dispose();
    widget.controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: widget.controller,
      builder: (context, _) {
        final controller = widget.controller;
        return Scaffold(
          appBar: AppBar(title: const Text('Assistente Diversa')),
          body: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 760),
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    DropdownButtonFormField<String>(
                      value: controller.profile,
                      decoration: const InputDecoration(labelText: 'Perfil'),
                      items: const [
                        DropdownMenuItem(
                          value: 'professor',
                          child: Text('Professor'),
                        ),
                        DropdownMenuItem(
                          value: 'familia',
                          child: Text('Família'),
                        ),
                        DropdownMenuItem(value: 'gestor', child: Text('Gestor')),
                      ],
                      onChanged: (value) {
                        if (value != null) controller.selectProfile(value);
                      },
                    ),
                    const SizedBox(height: 16),
                    Expanded(
                      child: controller.messages.isEmpty
                          ? const Center(
                              child: Text(
                                'Faça uma pergunta sobre educação inclusiva.',
                              ),
                            )
                          : ListView.builder(
                              itemCount: controller.messages.length,
                              itemBuilder: (context, index) =>
                                  _MessageCard(message: controller.messages[index]),
                            ),
                    ),
                    if (controller.error case final error?)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: Text(
                          error,
                          style: TextStyle(color: Theme.of(context).colorScheme.error),
                        ),
                      ),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _messageController,
                            minLines: 1,
                            maxLines: 4,
                            onSubmitted: (_) => _submit(),
                            decoration: const InputDecoration(
                              hintText: 'Digite sua pergunta',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        IconButton.filled(
                          onPressed: controller.isSending ? null : _submit,
                          icon: controller.isSending
                              ? const SizedBox.square(
                                  dimension: 20,
                                  child: CircularProgressIndicator(strokeWidth: 2),
                                )
                              : const Icon(Icons.send),
                          tooltip: 'Enviar',
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  void _submit() {
    final text = _messageController.text;
    if (text.trim().isEmpty) return;
    _messageController.clear();
    widget.controller.send(text);
  }
}

class _MessageCard extends StatelessWidget {
  const _MessageCard({required this.message});

  final ChatMessage message;

  @override
  Widget build(BuildContext context) {
    final isUser = message.role == MessageRole.user;
    final colors = Theme.of(context).colorScheme;
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Card(
        color: isUser ? colors.primaryContainer : colors.surfaceContainerHighest,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 600),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(message.text),
                for (final source in message.sources)
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: SelectableText(
                      'Fonte: ${source.title} — ${source.sourceUrl}',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
