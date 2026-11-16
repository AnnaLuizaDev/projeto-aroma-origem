-- ============================================================================
-- PROJETO FÍSICO DO BANCO DE DADOS (MySQL 8.0+)
-- Sistema: E-commerce Cafeteria Gourmet (Grãos & Torra Especial)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS cafeteria_gourmet
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cafeteria_gourmet;

-- 1. Tabela de Clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Tabela de Endereços de Entrega
CREATE TABLE enderecos_entrega (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    cep CHAR(8) NOT NULL,
    logradouro VARCHAR(180) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    CONSTRAINT fk_endereco_cliente FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Tabela de Produtos (Cafés Especiais)
CREATE TABLE produtos_cafe (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    origem VARCHAR(100) NOT NULL,
    notas_sensoriais TEXT NOT NULL,
    intensidade TINYINT NOT NULL CHECK (intensidade BETWEEN 1 AND 10),
    data_torra DATE NOT NULL,
    preco_base DECIMAL(10, 2) NOT NULL,
    estoque_kg DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    ativo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

-- 4. Tabela de Pedidos
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_endereco INT NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('AGUARDANDO_PAGAMENTO', 'PAGO', 'EM_TORRA_MOAGEM', 'ENVIADO', 'ENTREGUE', 'CANCELADO')
        DEFAULT 'AGUARDANDO_PAGAMENTO',
    cupom_aplicado VARCHAR(30) NULL,
    valor_desconto DECIMAL(10, 2) DEFAULT 0.00,
    valor_frete DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    valor_total DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_pedido_endereco FOREIGN KEY (id_endereco) REFERENCES enderecos_entrega(id_endereco)
) ENGINE=InnoDB;

-- 5. Tabela de Itens do Pedido (com seleção obrigatória de moagem)
CREATE TABLE itens_pedido (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    tipo_moagem ENUM('GRAOS_INTEIROS', 'ESPRESSO', 'FILTRO_V60', 'PRENSA_FRANCESA', 'MOKA') NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10, 2) NOT NULL,
    taxa_moagem DECIMAL(10, 2) DEFAULT 0.00,
    CONSTRAINT fk_item_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_item_produto FOREIGN KEY (id_produto) REFERENCES produtos_cafe(id_produto)
) ENGINE=InnoDB;

-- 6. Tabela de Avaliações Sensoriais
CREATE TABLE avaliacoes_sensoriais (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    nota_estrelas TINYINT NOT NULL CHECK (nota_estrelas BETWEEN 1 AND 5),
    metodo_preparo VARCHAR(60),
    comentario TEXT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_aval_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_aval_produto FOREIGN KEY (id_produto) REFERENCES produtos_cafe(id_produto)
) ENGINE=InnoDB;

-- ============================================================================
-- INSERÇÃO DE DADOS INICIAIS PARA TESTES (SEED)
-- ============================================================================
INSERT INTO clientes (nome, email, senha_hash, telefone) VALUES
('Mariana Costa', 'mariana.cafe@email.com', '$2y$10$exemploHashSeguro123', '(11) 98888-1111'),
('Carlos Eduardo', 'carlos.barista@email.com', '$2y$10$exemploHashSeguro456', '(11) 97777-2222');

INSERT INTO enderecos_entrega (id_cliente, cep, logradouro, numero, bairro, cidade, uf) VALUES
(1, '09520010', 'Rua Goiás', '450', 'Centro', 'São Caetano do Sul', 'SP');

INSERT INTO produtos_cafe (nome, origem, notas_sensoriais, intensidade, data_torra, preco_base, estoque_kg) VALUES
('Blend Reserva Serra da Mantiqueira', 'Minas Gerais - Sul', 'Chocolate amargo, caramelo tostado e avelã', 8, CURDATE(), 54.90, 45.00),
('Microlote Bourbon Amarelo', 'Alta Mogiana - SP', 'Frutas amarelas, mel silvestre e acidez cítrica equilibrada', 6, CURDATE(), 68.50, 20.00),
('Geisha Edição Limitada', 'Caparaó - ES/MG', 'Jasmim, flor de laranjeira, pêssego e finalização doce', 5, CURDATE(), 92.00, 10.00),
('Intenso Espresso Barista', 'Cerrado Mineiro - MG', 'Cacau 70%, nozes e crema densa persistente', 9, CURDATE(), 49.90, 60.00);
