# KKK Windows Kurulum Betiği
$InstallDir = Get-Location
$ScriptPath = Join-Path $InstallDir "kkk.py"
$BatPath = Join-Path $InstallDir "kkk.bat"

Write-Host "🔧 Koduğum Kodunu Kurtar (KKK) kuruluyor..." -ForegroundColor Cyan

# 1. kkk.bat dosyasını oluştur (çalıştırıcı köprü)
$BatContent = "@echo off`npython `"$ScriptPath`" %*"
Set-Content -Path $BatPath -Value $BatContent

# 2. Mevcut klasörü Kullanıcı PATH değişkenine ekle
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($UserPath -like "*$InstallDir*") {
    Write-Host "⚠️  Bu klasör zaten PATH içinde kayıtlı." -ForegroundColor Yellow
} else {
    $NewPath = "$UserPath;$InstallDir"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "✅ Klasör kullanıcı PATH değişkenine eklendi." -ForegroundColor Green
}

Write-Host "--------------------------------------------------" -ForegroundColor White
Write-Host "🎉 Kurulum tamamlandı!" -ForegroundColor Green
Write-Host "🚀 Etkinleşmesi için yeni bir terminal (CMD veya PowerShell) açın." -ForegroundColor Cyan
Write-Host "Artık 'kkk' komutunu her yerde kullanabilirsiniz." -ForegroundColor White
