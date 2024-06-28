# Carrega o assembly System.Drawing
Add-Type -AssemblyName System.Drawing

# Define o caminho da imagem
$imagem = "C:\Users\julio\Documents\DB\prj\Campari\devel\python\campari_door_machine\flyer.png"

# Cria um objeto PrintDocument
$printDocument = New-Object System.Drawing.Printing.PrintDocument

# Define o evento de impressão
$printDocument_PrintPage = {
    param (
        [System.Object]$sender,
        [System.Drawing.Printing.PrintPageEventArgs]$e
    )

    # Carrega a imagem
    $image = [System.Drawing.Image]::FromFile($imagem)

    # Calcula o retângulo de destino para redimensionar a imagem para o tamanho da página
    $pageWidth = $e.PageSettings.PrintableArea.Width
    $pageHeight = $e.PageSettings.PrintableArea.Height
    $imageWidth = $image.Width
    $imageHeight = $image.Height

    # Calcula as proporções de redimensionamento
    $ratioX = $pageWidth / $imageWidth
    $ratioY = $pageHeight / $imageHeight
    $ratio = [Math]::Min($ratioX, $ratioY)

    # Calcula as novas dimensões da imagem
    $newWidth = [Math]::Round($imageWidth * $ratio)
    $newHeight = [Math]::Round($imageHeight * $ratio)

    # Calcula a posição para centralizar a imagem na página
    $x = ($pageWidth - $newWidth) / 2
    $y = ($pageHeight - $newHeight) / 2

    # Desenha a imagem na página de impressão
    $e.Graphics.DrawImage($image, $x, $y, $newWidth, $newHeight)

    # Libera recursos
    $image.Dispose()
}

# Adiciona o evento de impressão ao PrintDocument
$printDocument.add_PrintPage($printDocument_PrintPage)

# Imprime o documento
$printDocument.Print()
