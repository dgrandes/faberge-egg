program TVehiclesF;

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
  TwoVehicles in 'TwoVehicles.pas',
  Pairs in 'Pairs.pas',
  Flex in 'Flex.pas';

var

  rootpath: string;
  seq1,seq2: custarray;
  d1, d2: real;
  i,j,k:integer;

begin

  try
    delta:=2;

    Writeln('Initializing..');
    rootpath:='Instances\instance_21.txt';

    Writeln('Loading data..');
    Writeln('');

    load_cust(rootpath);
    clustering(cust);

    dist := dist_calc(cust);
    Writeln('');

  for j := 0 to length(vlist)-1 do
  for i :=0 to 1 do
  begin
    setlength(di,2);
    vlist[j].ve[i].custs := nneigh(vlist[j].ve[i].custs);
    Writeln(' ');

    vlist[j].ve[i].custs := _2_opt(vlist[j].ve[i].custs);
    Writeln(' ');
    Writeln(' ');

    di[i]:=explen(vlist[j].ve[i].custs,q,0);
    Writeln('Taking into account customer demand, the expected lenght of the'
              +' proposed sequence is '+floattostr(di[i]));
    Writeln(' ');
  end;

    Randomize;
    gen_demand(cust);

  for j := 0 to length(vlist)-1 do
  begin
    clock_counter(vlist[j]);
    fseq:=simulate(vlist[j]);
    d1:=0;
    Write('The final sequences followed were');
    for k := 0 to 1 do
      begin
        Write('0-');
        for I := 0 to length(fseq[k]) - 1 do Write(floattostr(fseq[k,i].ID)+'-') ;
        d2:=seq_length(fseq[k]);
        Writeln('0 ...and length '+floattostr(d2)+'.');
        d1:=d1+d2;
      end;
     Writeln('The total length travelled was '+floattostr(d1)+'.');
  end;

    Readln(input,rootpath);

  except
    on E:Exception do
      Writeln(E.Classname, ': ', E.Message);
  end;
end.
