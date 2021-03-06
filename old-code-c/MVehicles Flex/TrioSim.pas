unit TrioSim;

{$MODE Delphi}

interface

uses
SysUtils, math, ExpectedLen, Classes, Customers, Demands,
  Pairs,Flex, Subroutines, Vehicles, States, Typez, Rollout;

  function simulatet(var tr : trio):ccustarray;
  function updtet(var tr:trio; cstate:state; nnode:customer; d:boolean;i:integer):state;
  procedure switcht(var tr:trio;a:integer;b:integer);

implementation

function simulatet( var tr : trio):ccustarray;
var
cstate:state;
nnode,line:custarray;
anode,bnode,fnode:customer;
d:barray;
t,ad,bd,cd, fd,hd:boolean;
i,j,cq,ax:integer;
acost,bcost,ccost,dcost,fcost,gcost,hcost,ec:real;
minim:real;
sf,nexxt,ecost:rearray;
nseq:ccustarray;

begin
  setlength(line,3);
  for i:=0 to 2 do
  begin
    line[i]:=tr.line[i];
  end;
  cstate:= state.create(dep,q);
  cstate.dems:= dems;
  setlength(nnode,3);
  setlength(d,3);
  setlength(nexxt,3);
  setlength(ecost,3);
  setlength(fseq,3);
  setlength(nseq,3);
  setlength(sf,3);
  setlength(fs,3);
  t:=false;
  
  for i := 0 to 2 do
    begin
      setlength(fseq[i],0);
      setlength(nseq[i],length(tr.ve[i].custs));
      nseq[i]:=tr.ve[i].custs;
      mark_visited(nseq[i],dep);
      setlength(nseq[i],length(nseq[i])-1);
      apriori_length(nseq[i],cstate);

      //Define first node
      nseq[i]:= firstnode(nseq[i],tr.line[i],ec);
      ecost[i]:= ec;
      descrb(cstate);


      nnode[i]:=nseq[i,0];
      nexxt[i]:=dist[0,nnode[i].id];
      mark_visited(nseq[i],nnode[i]);
      setlength(nseq[i],length(nseq[i])-1);
      fs[i]:=-1;
    end;

  Writeln(' ');
  Writeln('Rolling out...');

  repeat //Define next customer
  begin

    //Who's next??
    minim:=infinity;
    i:=0;
    for j:=0 to 2 do
    begin
      sf[j]:= sofar(fseq[j])+nexxt[j];
      if ((sf[j]<minim) and (length(nseq[j])>0)) or (length(nseq[i])=0)then
      begin
        minim:= sf[j];
        i:=j;
      end;
    end;

    //Update the state
    cstate:= updtet(tr,cstate,nnode[i],d[i],i);
    descrb(cstate);

    fs[i]:=fs[i]+1;
    setlength(fseq[i],fs[i]+1);
    fseq[i,fs[i]]:=nnode[i];

    if length(nseq[i])>0 then
    begin
      acost:=0;  bcost:=0; ccost:=0; dcost:=0;
      fcost:=0;  gcost:=0; hcost:=0;

      //No switch
      anode:=roll(nseq[i],tr.line[i],tr.ve[i].cp,tr.ve[i].cq,ad,acost);

      if sf[i]>di[i]/2 then
      begin
        if i<>1 then
        begin
          //Switch
          bnode:=roll(nseq[1],tr.line[1],tr.ve[i].cp,tr.ve[i].cq,bd,bcost);
          for j := nnode[1].dem.dmin to nnode[1].dem.dmax do
          begin
            cq:= capac(tr.ve[1].cq,j,d[1]);
            roll(nseq[1],tr.line[1],tr.ve[1].cp,cq,cd,dcost);
            ccost:=ccost+dcost;
          end;

        //Switch??
          if (bcost+ccost/nnode[1].dem.num)< (acost+ecost[1]) then
          begin
            nnode[i]:=bnode;
            ecost[i]:=bcost;
            d[i]:=bd;
            nexxt[i]:=next(tr.ve[i].cp,bnode,bd);
            switch(nseq,i,1);
            switcht(tr,i,1);
          end
          else
            begin
              nnode[i]:=anode;
              ecost[i]:=acost;
              d[i]:=ad;
              nexxt[i]:=next(tr.ve[i].cp,anode,ad);
            end;
        end
        else
        begin
          //Switch 1
          bnode:=roll(nseq[i-1],tr.line[i-1],tr.ve[i].cp,tr.ve[i].cq,bd,bcost);
          for j := nnode[i-1].dem.dmin to nnode[i-1].dem.dmax do
          begin
            cq:= capac(tr.ve[i-1].cq,j,d[i-1]);
            roll(nseq[i-1],tr.line[i-1],tr.ve[i-1].cp,cq,cd,dcost);
            ccost:=ccost+dcost;
          end;

          //Switch 2
          fnode:=roll(nseq[i+1],tr.line[i+1],tr.ve[i].cp,tr.ve[i].cq,fd,fcost);
          for j := nnode[i+1].dem.dmin to nnode[i+1].dem.dmax do
          begin
            cq:= capac(tr.ve[i+1].cq,j,d[i+1]);
            roll(nseq[i+1],tr.line[i+1],tr.ve[i+1].cp,cq,hd,hcost);
            gcost:=gcost+hcost;
          end;

          ax:=i-1;
          //Best switch?
         if bcost+ccost >fcost+gcost then
         begin
           bnode:=fnode;
           bcost:=fcost;
           bd:= fd;
           ax:=i+1;
         end;

        //Switch??
          if (bcost+ccost/nnode[ax].dem.num)< (acost+ecost[ax]) then
          begin
            nnode[i]:=bnode;
            ecost[i]:=bcost;
            d[i]:=bd;
            nexxt[i]:=next(tr.ve[i].cp,bnode,bd);
            switch(nseq,i,ax);
            switcht(tr,i,ax);
          end
          else
            begin
              nnode[i]:=anode;
              ecost[i]:=acost;
              d[i]:=ad;
              nexxt[i]:=next(tr.ve[i].cp,anode,ad);
            end;
        end;
      end
      else
      begin
         nnode[i]:=anode;
         ecost[i]:=acost;
         d[i]:=ad;
         nexxt[i]:=next(tr.ve[i].cp,anode,ad);
      end;

    mark_visited(nseq[i],nnode[i]);
    setlength(nseq[i],length(nseq[i])-1);

    //Last??
    if not((length(nseq[0])>0) or (length(nseq[1])>0)or (length(nseq[2])>0)) then
    begin
      for j := 0 to 2 do
      begin
        cstate:= updtet(tr,cstate,nnode[j],d[j],j);
        descrb(cstate);
        fs[j]:=fs[j]+1;
        setlength(fseq[j],fs[j]+1);
        fseq[j,fs[j]]:=nnode[j];
      end;
      t:=true;
    end;
  end;
  end;
  until t=true;

  result:=fseq;
  for i := 0 to 2 do
  begin
    tr.ve[i].cq:=Q;
    tr.ve[i].cp:=dep;
    tr.line[i]:=line[i];
  end;

end;

function updtet(var tr:trio; cstate:state; nnode:customer; d:boolean;i:integer):state;
var
nstate:state;
de:integer;

begin
  nstate :=state.create(nnode,tr.ve[i].cq);
  tr.ve[i].cp:=nnode;
  de:= cstate.dems[nnode.ID];
  //write('era '+inttostr(pe.ve[i].cq));
  nstate.dems:=cstate.dems;
  nstate.dems[nnode.ID]:=0;

  if d=false then  //New capacity
  begin
    if de>tr.ve[i].cq then
    begin
      //Have to go anyway
      nstate.cu_cap:=tr.ve[i].cq+q-de;
      tr.ve[i].cq:=tr.ve[i].cq+q-de;
      fs[i]:=fs[i]+1;
      setlength(fseq[i],fs[i]+1);
      fseq[i,fs[i]]:=nnode;
      fs[i]:=fs[i]+1;
      setlength(fseq[i],fs[i]+1);
      fseq[i,fs[i]]:=dep;
    end
    else
    begin
    nstate.cu_cap:=tr.ve[i].cq-de;
    tr.ve[i].cq:=tr.ve[i].cq-de;
    end;
  end
  else
  begin
    fs[i]:=fs[i]+1;
    setlength(fseq[i],fs[i]+1);
    fseq[i,fs[i]]:=dep;
    nstate.cu_cap:= q-de;
    tr.ve[i].cq:= q-de;
  end;
  //write(' y ahora es '+inttostr(pe.ve[i].cq));
  result:= nstate;
end;

procedure switcht(var tr:trio;a:integer;b:integer);
var
auxi:customer;
begin
   auxi:=tr.line[a];
   tr.line[a]:=tr.line[b];
   tr.line[b]:=auxi;
end;

end.
