unit Subroutines;


interface

  uses
  SysUtils, Classes, Customers, Demands, Vehicles, States, Typez;
  procedure load_cust(mydataname: string);
  function dist_calc(cust : custarray) : realarray;
  function seq_length(seq: custarray): real;
  function sofar(seq:custarray):real;
  function pdis(line:customer;point:customer):real;
  function c(index:integer;n1:integer):integer;
  procedure descrb(st:state);
  function iseven(num:integer):boolean;

  var
  cust : custarray;

implementation


procedure load_cust(mydataname: string);

var
index,i,j : integer;
xcoor, ycoor : real;
dem : demand;
tyype : integer;
a:integer;
b:real;
auxi: array[1..3,0..60]of real;
mydata : textfile;


begin

a:=6;     //Num of case within the file
b:=0.75;
ed:=3;

assignfile(mydata, mydataname);
Reset(mydata);

for i := 1 to 3*a do readln(mydata);

for I := 1 to 3 do
begin
j:=-1;
repeat
begin
    j:=j+1;
    read(mydata, xcoor);
    auxi[i,j]:=xcoor;
end;
until eoln(mydata);
end;
Closefile(mydata);

setlength(cust,101);

for index := 0 to j do
begin
  xcoor := auxi[1,index];
  ycoor := auxi[2,index];
  tyype := trunc(auxi[3,index]);
  if index=0 then
  begin
    dem := demand.create(0,0);
    dep:= customer.create(index,xcoor,ycoor,dem);
    cust[index]:= customer.create(index, xcoor, ycoor, dem);
  end
  else
  begin
  case tyype of
    0: dem := demand.create(3,1);
    1: dem := demand.create(4,2);
    2: dem := demand.create(5,3);
  end;

  cust[index]:= customer.create(index, xcoor, ycoor, dem);
  WriteLn('Customer '+inttostr(cust[index].ID) +' is located at '+ floattostr(xcoor)+
  ',' +floattostr(ycoor)+ ' and has demand type '+floattostr(tyype)+'.');
  end;

end;

n:=j+1;
Q:=round(ed*(n-1)/(v*(b+1)));
Writeln('The capacity of the vehicle(s) is '+floattostr(q)+' units');

setlength(cust,n);
end;

function dist_calc(cust : custarray) : realarray;
var
i,j : integer;

begin
        setlength(dist,n,n);
        For i := 0 To n-1 do
        begin
            Writeln(' ');
            For j := i To n-1 do
            begin
              dist[i, j] := sqrt(sqr(cust[i].xcoor - cust[j].xcoor)
                + sqr(cust[i].ycoor - cust[j].ycoor));
              dist[j,i] := dist[i,j];
              Write(floattostr(dist[i,j]));
            end;
        end;
result := dist;
end;

function seq_length(seq: custarray): real;
var
dis :real;
i,n1 : integer;
begin
  n1:= length(seq);
  dis:= dist[0,seq[0].ID];
  for I := 0 to n1 - 2 do dis:=dis+ dist[seq[i].ID,seq[i+1].ID];
  dis:= dis + dist[seq[n1-1].ID,0];
  result := dis;
end;

function sofar(seq: custarray): real;
var
dis :real;
i,n1 : integer;
begin
  n1:= length(seq);
  if n1>0 then
  begin
    dis:= dist[0,seq[0].ID];
    for I := 0 to n1 - 2 do dis:=dis+ dist[seq[i].ID,seq[i+1].ID];
    result := dis;
  end
  else result:=0;
end;

function c(index:integer;n1:integer):integer;
begin
  if index>n1-1 then
  begin
    result := index - n1;
  end
  else
    result:= index;
end;

function pdis(line:customer;point:customer):real;
var
a,b,m,n:real;
begin
    a:=line.xcoor;
    b:= -line.ycoor;
    m:= point.xcoor;
    n:=point.ycoor;

    if line =dep then
    begin
      result := dist[dep.ID, point.ID]/2;
    end
    else result:= abs(a*m+b*n)/sqrt(sqr(a)+sqr(b));
end;

function iseven(num:integer):boolean;
begin
  if num/2 = round(num/2) then
  begin
    result:=true;
  end
  else result:=false;
end;

procedure descrb(st:state);
var
i:integer;
begin
  Write('Current state is ('+floattostr(st.cu_pos.ID)+',');
  for I := 1 to n - 1 do Write(floattostr(st.dems[i])+',');
  Writeln(floattostr(st.cu_cap)+')');
end;

{procedure QuickSort(var A: array of real; iLo, iHi: Integer) ;
 var
   Lo, Hi, Pivot, T: integer;
 begin
   Lo := iLo;
   Hi := iHi;
   Pivot := A[(Lo + Hi) div 2];
   repeat
     while A[Lo] < Pivot do Inc(Lo) ;
     while A[Hi] > Pivot do Dec(Hi) ;
     if Lo <= Hi then
     begin
       T := A[Lo];
       A[Lo] := A[Hi];
       A[Hi] := T;
       Inc(Lo) ;
       Dec(Hi) ;
     end;
   until Lo > Hi;
   if Hi > iLo then QuickSort(A, iLo, Hi) ;
   if Lo < iHi then QuickSort(A, Lo, iHi) ;
 end; }

end.
