Idea: Build up a script that scans each file for a "syz_" function call,
then prepend the "syz_prepare_data" call if it's not already there. But only
do that for the changes inside "<<<<<< HEAD" and "========="; blast away
the printfuzz changes.
