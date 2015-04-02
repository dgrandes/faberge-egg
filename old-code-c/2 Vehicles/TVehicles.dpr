program TVehicles;

{$APPTYPE CONSOLE}

uses
  SysUtils,
  Customers in 'Customers.pas',
  Demands in 'Demands.pas',
  ExpectedLen in 'ExpectedLen.pas',
  Heuristics in 'Heuristics.pas',
  Rollout in 'Rollout.pas',
  States in 'States.pas',
  Subroutines in 'Subroutines.pas',
  Typez in 'Typez.pas',
  Vehicles in 'Vehicles.pas',
  TwoVehicles in 'TwoVehicles.pas';

var

  rootpath: string;
  custs : custarray;
  seq1,seq2, fseq : custarray;
  d: real;
  i,j:integer;

begin

  try
    { TODO -oUser -cConsole Main : Insert code here }
    Writeln('Initializing..');
    rootpath:='Instances\instance_21.txt';

    Writeln('Loading data..');
    Writeln('');

    custs:= load_cust(rootpath);
    clustering(custs);

    dist := dist_calc(custs);
    Writeln('');

  for j := 0 to 1 do
  begin
    seq1 := nneigh(vlist[j].custs);
    Writeln('');

    seq2 := _2_opt(seq1);
    Writeln('');
    Writeln('');

    d:=explen(seq2,q,0);
    Writeln('Taking into account customer demand, the expected lenght of the'
              +' proposed sequence is '+floattostr(d));
    Writeln(' ');

    Randomize;
    fseq:=roll(seq2);

    Write('The final sequence followed was 0-');
    for I := 0 to length(fseq) - 1 do Write(floattostr(fseq[i].ID)+'-') ;

    d:=seq_length(fseq);
    Writeln('0 ...and the total length travelled was '+floattostr(d)+'.');

  end;

    Readln(input,rootpath);

  except
    on E:Exception do
      Writeln(E.Classname, ': ', E.Message);
  end;
end.
