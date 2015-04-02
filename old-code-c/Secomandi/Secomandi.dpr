program Secomandi;

{$APPTYPE CONSOLE}

uses
  SysUtils,
  Classes,
  Customers in 'Customers.pas',
  Vehicles in 'Vehicles.pas',
  Subroutines in 'Subroutines.pas',
  Demands in 'Demands.pas',
  Rollout in 'Rollout.pas',
  ExpectedLen in 'ExpectedLen.pas',
  Heuristics in 'Heuristics.pas',
  Typez in 'Typez.pas',
  States in 'States.pas';

//States in 'States.pas';

var

  rootpath: string;
  custs : custarray;
  seq1,seq2, fseq : custarray;
  d: real;
  i:integer;

begin

  try
    { TODO -oUser -cConsole Main : Insert code here }
    Writeln('Initializing..');
    rootpath:='Instances\instance_61.txt';

    Writeln('Loading data..');
    Writeln('');

    custs:= load_cust(rootpath);

    dist := dist_calc(custs);
    Writeln('');

    seq1 := nneigh(custs);
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


    Readln(input,rootpath);

  except
    on E:Exception do
      Writeln(E.Classname, ': ', E.Message);
  end;
end.
