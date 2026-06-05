# Render the real Excel worksheets to PNG using Microsoft Excel itself (COM),
# for true Excel fidelity (fonts, gridlines, the real orange fill).
# Method: open workbook, CopyPicture the range, paste into a temp chart, export PNG.
# The Base Exclusion Funnel file ships blank, so we fill the verified answers in
# memory and close WITHOUT saving (the original file is never modified).
#
# Source files live in C:\Users\raeda\Downloads. Output goes to _tools\excel_real,
# then the optimizer copies them into slides\excel\.
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Windows.Forms
Get-Process EXCEL -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
$excel = New-Object -ComObject Excel.Application
$excel.Visible=$false; $excel.DisplayAlerts=$false
$dl='C:\Users\raeda\Downloads'
$out='C:\Users\raeda\Downloads\PM_Final_StudyBook\_tools\excel_real'
New-Item -ItemType Directory -Force -Path $out | Out-Null

function Shoot($ws,$rangeAddr,$outPng){
  $rng=$ws.Range($rangeAddr)
  for($t=1;$t -le 3;$t++){
    $rng.CopyPicture(1,2); [System.Windows.Forms.Application]::DoEvents(); Start-Sleep -Milliseconds 800
    $co=$ws.ChartObjects().Add(0,0,$rng.Width,$rng.Height)
    $co.Chart.ChartArea.Format.Line.Visible=$false
    $co.Activate(); [System.Windows.Forms.Application]::DoEvents()
    try{ $co.Chart.Paste() }catch{}
    [System.Windows.Forms.Application]::DoEvents(); Start-Sleep -Milliseconds 800
    try{ $co.Chart.Export($outPng,'PNG') | Out-Null }catch{}
    $co.Delete()
    if((Test-Path $outPng) -and (Get-Item $outPng).Length -gt 3000){ break }
  }
}
try {
  $wb=$excel.Workbooks.Open("$dl\Pricing Games.xlsx",$false,$true); $ws=$wb.Worksheets.Item(1); $ws.Activate()
  Shoot $ws 'B2:N13' (Join-Path $out 'pricing_excel.png'); $wb.Close($false)

  $wb=$excel.Workbooks.Open("$dl\Designing Your Own Products.xlsx",$false,$true); $ws=$wb.Worksheets.Item(1); $ws.Activate()
  Shoot $ws 'B1:H57' (Join-Path $out 'design_excel.png'); $wb.Close($false)

  $wb=$excel.Workbooks.Open("$dl\Base Funnal Analysis Data.xlsx",$false,$true); $ws=$wb.Worksheets.Item(1); $ws.Activate()
  Shoot $ws 'A1:M11' (Join-Path $out 'data_excel.png'); $wb.Close($false)

  # Funnel: fill verified answers in memory, format percentages, render, close WITHOUT saving.
  $wb=$excel.Workbooks.Open("$dl\Base Exclusion Funnel.xlsx",$false,$false); $ws=$wb.Worksheets.Item(1); $ws.Activate()
  $ws.Range('C17').Value2=1; $ws.Range('C18').Value2=368; $ws.Range('C20').Value2=350; $ws.Range('C21').Value2=20
  $ws.Range('D27').Value2=158039
  $ws.Range('E27').Value2=5659;  $ws.Range('F27').Value2=9487;  $ws.Range('G27').Value2=142893; $ws.Range('H27').Value2=15146
  $ws.Range('I27').Value2=3924;  $ws.Range('J27').Value2=6648;  $ws.Range('K27').Value2=147467; $ws.Range('L27').Value2=10572
  $ws.Range('M27').Value2=3924;  $ws.Range('N27').Value2=6648;  $ws.Range('O27').Value2=140827; $ws.Range('P27').Value2=17212
  $ws.Range('D26:P26').NumberFormat='0.00%'
  $excel.CalculateFull(); Start-Sleep -Milliseconds 400
  Shoot $ws 'B2:P27' (Join-Path $out 'funnel_excel.png'); $wb.Close($false)
} finally { $excel.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null }
Write-Output "Rendered 4 sheets to $out"
