CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT NOT NULL,
    keywords TEXT[] NOT NULL DEFAULT '{}',
    embedding VECTOR(384),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS articles_embedding_cosine_idx
    ON articles USING hnsw (embedding vector_cosine_ops);

INSERT INTO articles (id, title, summary, content, source_url, keywords)
VALUES
    (
        'mock-inclusao-escolar',
        'Princípios da educação inclusiva',
        'A educação inclusiva remove barreiras à participação e à aprendizagem e considera as necessidades de cada estudante no planejamento pedagógico.',
        'Escolas inclusivas identificam e reduzem barreiras físicas, comunicacionais, pedagógicas e atitudinais. O planejamento deve promover participação, aprendizagem e convivência de todos os estudantes.',
        'https://diversa.org.br/',
        ARRAY['educação inclusiva', 'inclusão', 'barreiras', 'participação', 'aprendizagem', 'escola']
    ),
    (
        'mock-aee',
        'Atendimento Educacional Especializado (AEE)',
        'O Atendimento Educacional Especializado complementa ou suplementa a formação do estudante e deve estar articulado à proposta pedagógica da escola.',
        'O AEE identifica recursos de acessibilidade e estratégias que favorecem a participação e a autonomia. Ele não substitui a escolarização em classe comum e requer articulação entre profissionais, estudante e família.',
        'https://diversa.org.br/',
        ARRAY['AEE', 'atendimento educacional especializado', 'acessibilidade', 'autonomia', 'recursos', 'sala de recursos']
    ),
    (
        'mock-tea',
        'Apoio a estudantes autistas',
        'O apoio a estudantes autistas deve considerar suas características individuais, oferecer comunicação acessível e organizar rotinas previsíveis com participação do estudante.',
        'Estratégias podem incluir antecipação de mudanças, recursos visuais, diferentes formas de comunicação e ajustes sensoriais. As decisões devem ser individualizadas e construídas com o estudante, a família e a equipe escolar.',
        'https://diversa.org.br/',
        ARRAY['autismo', 'autista', 'TEA', 'comunicação', 'rotina', 'apoio', 'acessibilidade']
    )
ON CONFLICT (id) DO NOTHING;
