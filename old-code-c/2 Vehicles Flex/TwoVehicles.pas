unit TwoVehicles;

interface

 uses
 sysUtils, Typez, vehicles, customers, math, pairs;

  procedure clustering(clist:custarray);
  function angle(clist:custarray):polararray;
  procedure SortPArray(parray:polararray);
  function exp_dem(cu:customer): real;

 var
 vlist: parray;
 v,p:integer;
 delta:real;

implementation

procedure clustering(clist:custarray);
var
i:integer;
aux1,aux2: custarray;
ve:vearray;
poarr: polararray;
cap:real;
line:customer;

begin
   poarr:=angle(clist);
   SortPArray(poarr);
   setlength(vlist,1);
   setlength(ve,2);
   setlength(aux1,1);
   setlength(aux2,1);
   aux1[0]:=dep;
   aux2[0]:=dep;
   v:=2;
   p:=1;
   cap:=0;

  for i := 0 to length(poarr) - 1 do
  if cap+exp_dem(poarr[i].cust) < 3*(n-1)/2 then
  begin
      setlength(aux1, length(aux1)+1);
      aux1[length(aux1)-1]:=poarr[i].cust;
      cap:=cap + exp_dem(poarr[i].cust);
      line:=poarr[i].cust;
  end
  else
  begin
      cap:=cap + exp_dem(poarr[i].cust);
      setlength(aux2, length(aux2)+1);
      aux2[length(aux2)-1]:=poarr[i].cust;
  end;
  ve[0]:= vehicle.create(1,dep,aux1,q);
  ve[1]:=vehicle.Create(2,dep,aux2,q);
  vlist[0]:= pair.create(p,ve,line);
end;

function angle(clist:custarray):polararray;
var
i:integer;
ang:real;
polar:polararray;
begin
     setlength(polar,n-1);
     for i := 1 to n - 1 do
     begin
     ang:= arctan(abs(clist[i].ycoor/clist[i].xcoor));

     if clist[i].ycoor<0 then
      if clist[i].xcoor<0 then
      begin
        ang:=ang+PI;
      end
      else ang:=2*PI - ang;

     if clist[i].ycoor>0 then
      if clist[i].xcoor<0 then
      begin
        ang:=PI-ang;
      end;
      polar[i-1].cust:=clist[i];
      polar[i-1].ang:=ang;
     end;
     result:=polar;
end;

procedure SortPArray(parray:polararray);
var
p2: Integer;
temp : polar_coor;
swaps: boolean;
begin
swaps:=true;
while swaps=true do
  begin
  swaps:=false;
  for p2 := 0 to length(parray) - 2 do
  begin
    if (parray[p2].ang > parray[p2+1].ang) then
    begin
      swaps:=true;
      temp := parray[p2];
      parray[p2] := parray[p2+1];
      parray[p2+1] := temp;
    end;
  end;
  end;
end;

function exp_dem(cu:customer): real;
begin
  result:=(cu.dem.dmax+cu.dem.dmin)/2;
end;



{i:integer;
aux1,aux2: custarray;
begin
    setlength(vlist,2);
    setlength(aux1,1);
    setlength(aux2,1);
    aux1[0]:=dep;
    aux2[0]:=dep;

    for I := 1 to length(clist) - 1 do
    if clist[i].xcoor<clist[i].ycoor then
    begin
        setlength(aux1, length(aux1)+1);
        aux1[length(aux1)-1]:=clist[i];
    end
    else
    begin
        setlength(aux2, length(aux2)+1);
        aux2[length(aux2)-1]:=clist[i];
    end;

    vlist[0]:= vehicle.create(1,aux1);
    vlist[1]:=vehicle.Create(2,aux2);}
end.