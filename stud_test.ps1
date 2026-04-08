# Get start time with high precision
$start_time = Get-Date

Clear-Host
cd venv\Scripts
.\activate
cd ..\..

# Set PYTHONPATH and run the test script
$env:PYTHONPATH = "./app"
#python test.py
##python testXarpusScreech.py
##python XarpDefReduc.py
##python SpecTest.py
##python NyloBossDamage.py
##python XarpDefEffects.py
##python XarpWrSim.py
python XarpScythingSims.py

# Calculate and display duration
$end_time = Get-Date
$duration = $end_time - $start_time
Write-Output ""
Write-Output "---------------------------------------"
Write-Output ("Script execution time: {0:N6} seconds" -f $duration.TotalSeconds)