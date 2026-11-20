-- CreateTable
CREATE TABLE "PvpSala" (
    "id" TEXT NOT NULL,
    "codigo" TEXT NOT NULL,
    "modo" TEXT NOT NULL,
    "nivel" INTEGER NOT NULL,
    "estado" TEXT NOT NULL DEFAULT 'esperando',
    "datos" JSONB NOT NULL,
    "expiraEn" TIMESTAMP(3) NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "actualizadoEn" TIMESTAMP(3) NOT NULL,
    CONSTRAINT "PvpSala_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "PvpSala_codigo_key" ON "PvpSala"("codigo");

-- CreateIndex
CREATE INDEX "PvpSala_estado_modo_nivel_creadoEn_idx" ON "PvpSala"("estado", "modo", "nivel", "creadoEn");

-- CreateIndex
CREATE INDEX "PvpSala_expiraEn_idx" ON "PvpSala"("expiraEn");
