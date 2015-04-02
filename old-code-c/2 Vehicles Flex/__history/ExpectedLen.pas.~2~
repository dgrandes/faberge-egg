unit ExpectedLen;

interface

  uses
  SysUtils, Math, Classes, Customers, Demands,
  Subroutines, States, Vehicles, Typez;
  function explen(seq:custarray; cq, i :integer):real;
  function prob(cus: customer; dem:integer):real;
  function go_notgo(seq:custarray;cq,i:integer):rearray;
  function exp_length(seq:custarray; cq, i :integer):real;
  procedure ini_elen(n1:integer);

  var
  elen : realarray;

implementation

function explen(seq:custarray; cq, i:integer):real;
begin
  ini_elen(length(seq));
  result:=exp_length(seq,cq,i);
end;

procedure ini_elen(n1:integer);
var
i,j:integer;
begin
  setlength(elen,q+1,n1);
  for I := 0 to q do
    for j := 0 to n1-1 do
      begin
        elen[i,j]:=0;
      end;
end;

function exp_length(seq:custarray; cq, i:integer):real;
var
n1:integer;
go_ng: rearray;

begin
  //Writeln('Calling with cq='+inttostr(cq)+' and i='+inttostr(i));
  n1:= length(seq);
  setlength(go_ng,2);
  if elen[cq,i]=0 then
  begin
    if i< n1-1 then
    begin
      go_ng:=go_notgo(seq,cq,i);
     //Best decision
      elen[cq,i]:= min(go_ng[0],go_ng[1]);
    end
    else
    begin
      elen[cq,i]:=dist[0,seq[n1-1].ID];
    end;
  end;
  result:=elen[cq,i];

//  Writeln(floattostr(result));
end;

function go_notgo(seq:custarray;cq,i:integer):rearray;
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
           // Writeln('nexc while i='+inttostr(i)+' and j='+inttostr(j));
          nexc:=nexc +exp_length(seq,cq-j,i+1)*prob(seq[i+1],j);
          end
          else
            //Exceeding capacity in next stop
          begin
            //Writeln('exc while i='+inttostr(i)+' and j='+inttostr(j));
            exc:=exc +prob(seq[i+1],j)*(2*dist[0,seq[i+1].ID]+exp_length(seq,q+cq-j,i+1));
          end;
      //Writeln('tps while i='+inttostr(i)+' and j='+inttostr(j));
      tps:=tps+exp_length(seq,Q-j,i+1)*prob(seq[i+1],j);
    end;
    //If I don't go to the depot before next stop
    go_ng[0]:=dist[seq[i].ID,seq[i+1].ID] + nexc + exc;
    //If I go to the depot at this point
    go_ng[1]:=dist[seq[i].ID,0]+dist[0,seq[i+1].ID]+tps;

    result:= go_ng;
end;

function prob(cus: customer; dem:integer):real;
    var
    proba:real;
    begin
      if (cus.dem.dmin<=dem) and (dem<=cus.dem.dmax) then
      begin
        proba:=(1/cus.dem.num);
      end
      else
        begin
          proba:=0;
        end;

      result:=proba;
    end;
end.
