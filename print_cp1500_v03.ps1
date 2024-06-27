# Carrega o assembly System.Drawing
Add-Type -AssemblyName System.Drawing

# Define o caminho da imagem
# $imagem = "C:\db\savedImage2.png"
#$imagem = "C:\Users\julio\Documents\DB\prj\OBoticario\DiaDasMaes\unity\oboticario_maes_unity\Assets\StreamingAssets\savedImage.png"
$imagem = "C:\Users\julio\Documents\DB\prj\Campari\devel\python\campari_door_machine\flyer.png"

# Cria um objeto PrintDocument
$printDocument = New-Object System.Drawing.Printing.PrintDocument


$printDocument = new-object System.Drawing.Printing.PrintDocument
$printDocument.DefaultPageSettings.Margins.Left = 0
$printDocument.DefaultPageSettings.Margins.Right = 0
$printDocument.DefaultPageSettings.Margins.Top = 0
$printDocument.DefaultPageSettings.Margins.Bottom = 0

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
    $ratio = $ratio * 0.935

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

Write-Host "Printing $imagem..."

# Imprime o documento
$printDocument.Print()