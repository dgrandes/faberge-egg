unit TwoVehicles;

interface

 uses
 sysUtils, typez, vehicles, customers,subroutines, math, pairs;

  procedure clustering(clist:custarray);
  function angle(clist:custarray):polararray;
  procedure SortPArray(parray:polararray);
  function exp_dem(cu:customer): real;

  var
  vlist: parray;
  tr: trio;

implementation

procedure clustering(clist:custarray);
var
i,k,j,vc,par, n2:integer;
aux: ccustarray;
ve:vearray;
poarr: polararray;
cap:real;
a:boolean;
line:customer;
li:custarray;

begin
   poarr:=angle(clist);
   SortPArray(poarr);
   setlength(vlist,0);
   setlength(aux,2,1);
   setlength(ve,2);
   p:=-1;   vc:=0;   cap:=0;  par:=3; t:=0; i:=0;

   a:=iseven(v);
   if a=true then par:=0;

  while vc<v-par do
  begin
  setlength(vlist,length(vlist)+1);
    j:=0;
    while j<2 do
    begin
      aux[j,0]:=dep;
      if vc<v-1 then
      begin
        repeat
        begin
          setlength(aux[j], length(aux[j])+1);
          aux[j][length(aux[j])-1]:=poarr[i].cust;
          cap:=cap + exp_dem(poarr[i].cust);
          if j=0 then line:=poarr[i].cust;
          i:=i+1;
        end;
        until cap + exp_dem(poarr[i].cust)/2 > ed*(n-1)/v;
      end
      else
      begin
        for k := i to length(poarr) - 1 do
        begin
          setlength(aux[j], length(aux[j])+1);
          aux[j][length(aux[j])-1]:=poarr[k].cust;
        end;
      end;
      j:=j+1;  vc:=vc+1;  cap:=0;
    end;
    ve[0]:= vehicle.create(vc-1,dep,aux[0],q);
    ve[1]:=vehicle.Create(vc,dep,aux[1],q);
    p:=p+1;
    vlist[p]:= pair.create(p,ve,line);
    setlength(aux,2,1);
  end;

  if par<>0 then
  begin
    setlength(aux,3,1);
    setlength(ve,3);
    setlength(li,3);
    j:=0;
    for k := 0 to 2 do  aux[k,0]:=dep;

    repeat
      begin
        setlength(aux[j], length(aux[j])+1);
        aux[j][length(aux[j])-1]:=poarr[i].cust;
        cap:=cap + exp_dem(poarr[i].cust);
        li[j]:=poarr[i].cust;
        i:=i+1;
      end;
    until cap +exp_dem(poarr[i].cust)/2> ed*(n-1)/v;
    j:=j+1;  vc:=vc+1;  cap:=0;
    n2:=length(poarr)-1;
    repeat
      begin
        setlength(aux[j], length(aux[j])+1);
        aux[j][length(aux[j])-1]:=poarr[n2].cust;
        cap:=cap + exp_dem(poarr[n2].cust);
        li[j+1]:=poarr[n2].cust;
        n2:=n2-1;
      end;
    until cap + exp_dem(poarr[i].cust)/2 > ed*(n-1)/v;
    j:=j+1;  vc:=vc+1;
    for k := i to n2 do
    begin
      setlength(aux[j], length(aux[j])+1);
      aux[j][length(aux[j])-1]:=poarr[k].cust;
    end;
    li[1]:=dep;
    ve[0]:= vehicle.create(vc-1,dep,aux[0],q);
    ve[1]:=vehicle.Create(vc,dep,aux[2],q);
    ve[2]:=vehicle.Create(vc+1,dep,aux[1],q);
    tr:= trio.create(ve,li);
  end;

 {for i := 0 to length(poarr) - 1 do
  begin
    if not (vc>v-par) then
    begin
      if j<2 then
      begin
        while cap+exp_dem(poarr[i].cust) < ed*(n-1)/v do
        begin
          setlength(aux[j], length(aux[j])+1);
          aux[j][length(aux[j])-1]:=poarr[i].cust;
          cap:=cap + exp_dem(poarr[i].cust);
          if j=0 then line:=poarr[i].cust;
        end;
        j:=j+1;  vc:=vc+1;  cap:=0;
      end;
      ve[0]:= vehicle.create(vc-1,dep,aux[0],q);
      ve[1]:=vehicle.Create(vc,dep,aux[1],q);
      p:=p+1;  j:=0;
      vlist[0]:= pair.create(p,ve,line);
      setlength(aux,2,1);
    end
    else
    setlength(aux,3,1);
    setlength(ve,3);
    setlength(li,2,1);
    if j<3 then
      begin
        while cap+exp_dem(poarr[i].cust) < ed*(n-1)/v do
        begin
          setlength(aux[j], length(aux[j])+1);
          aux[j][length(aux[j])-1]:=poarr[i].cust;
          cap:=cap + exp_dem(poarr[i].cust);
          if j<>2 then li[j]:=poarr[i].cust;
        end;
        j:=j+1;  vc:=vc+1;  cap:=0;
      end;
      ve[0]:= vehicle.create(vc-1,dep,aux[0],q);
      ve[1]:=vehicle.Create(vc,dep,aux[1],q);
      ve[2]:=vehicle.Create(vc-2,dep,aux[2],q);
      t:=1;  j:=0;
      tr := trio.create();
  end;     }

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
