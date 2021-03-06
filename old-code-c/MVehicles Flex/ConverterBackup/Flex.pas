unit Flex;

interface

uses
  Sysutils, Customers, pairs,vehicles, math, subroutines, expectedlen, typez;

    procedure clock_counter(var pa:pair);
    function cost(load:integer;pos:customer;line:customer):real;
    function expcos(seq:custarray; cq, i:integer;l:customer):real;
    procedure ini_cos(n1:integer);
    function exp_cost(seq:custarray; cq, i:integer;l:customer):real;
    function cgo_notgo(seq:custarray;cq,i:integer;l:customer):rearray;
    procedure clock_countert(var tr:trio);

var
delta:real;
cos:realarray;

implementation

function expcos(seq:custarray; cq, i:integer;l:customer):real;
begin
  ini_cos(length(seq));
  result:=exp_cost(seq,cq,i,l);
end;

procedure ini_cos(n1:integer);
var
i,j:integer;
begin
  setlength(cos,q+1,n1);
  for I := 0 to q do
    for j := 0 to n1-1 do
      begin
        cos[i,j]:=0;
      end;
end;

function exp_cost(seq:custarray; cq, i:integer;l:customer):real;
var
n1:integer;
go_ng: rearray;

begin
  n1:= length(seq);
  //Writeln('Calling with cq='+inttostr(cq)+' n1:='+inttostr(n1)+' and i='+inttostr(i));
  setlength(go_ng,2);
  if cos[cq,i]=0 then
  begin
    if i< n1-1 then
    begin
      go_ng:=cgo_notgo(seq,cq,i,l);
     //Best decision
      cos[cq,i]:= min(go_ng[0],go_ng[1])+cost(cq,seq[i],l);
    end
    else
    begin
      cos[cq,i]:=dist[0,seq[n1-1].ID]+cost(cq,seq[n1-1],l);
    end;
  end;
  result:=cos[cq,i];

//  Writeln(floattostr(result));
end;

function cgo_notgo(seq:custarray;cq,i:integer;l:customer):rearray;
var
nexc,exc,tps:real;
j:integer;
go_ng:rearray;

begin
    setlength(go_ng,2);
    nexc:=0;
    exc:=0;
    tps:=0;

    for j:= seq[i+1].dem.dmin to seq[i+1].dem.dmax do
    begin
      if j<= cq then
          begin
            //Not exceeding capacity in next stop
           //Writeln('nexc while i='+inttostr(i)+' and j='+inttostr(j));
          nexc:=nexc +exp_cost(seq,cq-j,i+1,l)*prob(seq[i+1],j);
          end
          else
            //Exceeding capacity in next stop
          begin
            //Writeln('exc while i='+inttostr(i)+' and j='+inttostr(j));
            //writeln('q='+inttostr(q)+' and cq='+inttostr(cq));
            exc:=exc +prob(seq[i+1],j)*(2*dist[0,seq[i+1].ID]+exp_cost(seq,q+cq-j,i+1,l));
          end;
      //Writeln('tps while i='+inttostr(i)+' and j='+inttostr(j));
      tps:=tps+exp_cost(seq,Q-j,i+1,l)*prob(seq[i+1],j);
    end;
    //If I don't go to the depot before next stop
    go_ng[0]:=dist[seq[i].ID,seq[i+1].ID] + nexc + exc;
    //If I go to the depot at this point
    go_ng[1]:=dist[seq[i].ID,0]+dist[0,seq[i+1].ID]+tps;

    result:= go_ng;
end;


procedure clock_counter(var pa:pair);
var
i,j,n1:integer;
aux2:custarray;
begin
  for j := 0 to 1 do
  begin
    n1:= length(pa.ve[j].custs);
    setlength(aux2,n1);
    aux2[0]:=dep;

    for I := 1 to n1 -1  do
    begin
      aux2[n1-i]:=pa.ve[j].custs[i];
    end;
    if expcos(pa.ve[j].custs,q,0,pa.line)>expcos(aux2,q,0,pa.line) then
    begin
        pa.ve[j].custs:=aux2;
    end;
  end;
end;

procedure clock_countert(var tr:trio);
var
i,j,n1:integer;
aux2:custarray;
begin
  for j := 0 to 2 do
  begin
    n1:= length(tr.ve[j].custs);
    setlength(aux2,n1);
    aux2[0]:=dep;

    for I := 1 to n1 -1  do
    begin
      aux2[n1-i]:=tr.ve[j].custs[i];
    end;
    if expcos(tr.ve[j].custs,q,0,tr.line[j])>expcos(aux2,q,0,tr.line[j]) then
    begin
        tr.ve[j].custs:=aux2;
    end;
  end;
end;

function cost(load:integer;pos:customer;line:customer):real;
var
d,per:real;
begin
  per:= power((load/q),3)+0.000001;
  d:= pdis(line,pos);
   result:= delta*(1-2*per)*d;
end;
end.
