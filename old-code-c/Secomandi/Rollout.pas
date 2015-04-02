unit Rollout;

interface

uses
  SysUtils, math, expectedlen, Classes, Customers, Demands,
  Subroutines, Vehicles, States, Typez;
  function roll(seq:custarray):custarray;
  function firstnode(seq:custarray):custarray;
  function updte(cstate:state; nnode:customer; d:boolean):state;
  procedure mark_visited(seq:custarray;node:customer);
  function gen_demand(seq:custarray):intarray;
  procedure apriori_length(seq:custarray;st:state);

 var
 fseq:custarray;
 fs:integer;

implementation

function roll(seq:custarray):custarray;
var
cstate:state;
nnode, nnotgo,ngo:customer;
go,notgo, cnotgo,cgo:real;
d,t:boolean;
i,j:integer;
nseq,aseq:custarray;
go_ng: rearray;

begin

  setlength(nseq,length(seq));
  nseq:=seq;
  Writeln(' ');
  Writeln('Generating demand...');
  cstate:= state.create(dep,q);
  cstate.dems:= gen_demand(seq);

  mark_visited(nseq,dep);
  setlength(nseq,length(nseq)-1);

  //Define first node
  nseq:= firstnode(nseq);
  descrb(cstate);
  apriori_length(nseq,cstate);

  nnode:=nseq[0];
  mark_visited(nseq,nnode);
  setlength(nseq,length(nseq)-1);

  cstate:= updte(cstate,nnode,false);
  setlength(fseq,1);
  fseq[0]:=nnode;

  setlength(go_ng,2);
  fs:=0;

  Writeln(' ');
  Writeln('Rolling out...');
  descrb(cstate);
  repeat //Define next customer
  begin

    notgo:=infinity;
    go:=infinity;

    for I := 0 to length(nseq)-1 do
    begin

    setlength(aseq,length(nseq)+1);
    for j := 0 to length(nseq) - 1 do aseq[j]:=nseq[c(1+j+i,length(nseq))];
    for j := length(aseq) - 2 downto 0 do aseq[j+1]:=aseq[j];
    aseq[0]:=nnode;

    ini_elen(length(aseq));
    go_ng:= go_notgo(aseq,cstate.cu_cap,0);

    //Straight to next customer
    cnotgo:= go_ng[0];
    if cnotgo<notgo then
    begin
      notgo:=cnotgo;
      nnotgo:=aseq[1];
    end;

  //Let's go to the depot first
    cgo:= go_ng[1];
    if cgo<go then
    begin
      go:=cgo;
      ngo:=aseq[1];
    end;
    end;

  //Best decision?
    if notgo<go then
    begin
      d:=false;
      nnode:=nnotgo;
      end
      else
      begin
        d:=true;
        nnode:=ngo;
        fs:=fs+1;
        setlength(fseq,fs+1);
        fseq[fs]:=dep;
    end;

  //Update the state
    mark_visited(nseq,nnode);
    setlength(nseq, length(nseq)-1);

    cstate:= updte(cstate,nnode,d);
    descrb(cstate);

    fs:=fs+1;
    setlength(fseq,fs+1);
    fseq[fs]:=nnode;

    //Termination?
    t:=true;
    for j := 1 to n - 1 do
      if cstate.dems[j]<>0 then
      begin
        t:=false;
    end;
  end;
  until t=true;

  result:=fseq;

end;

function gen_demand(seq:custarray):intarray;
var
dem:intarray;
i,j:integer;
f:real;
begin
    setlength(dem,length(seq));
    for j := 0 to length(seq) - 1 do
    begin
      randomize;
      f:=random;
      dem[seq[j].ID]:=seq[j].dem.dmax;
      for I := seq[j].dem.num-1 downto 1 do
        if f<(i/seq[j].dem.num) then
        begin
          dem[seq[j].id]:=seq[j].dem.dmax - (seq[j].dem.num-i);
        end;
    end;  
    result:=dem;
end;

procedure apriori_length(seq:custarray;st:state);
var
I,j:integer;
cq:integer;
apseq:custarray;
aseq:string;
td:real;
begin
   //First customer
   cq:=q;
   j:=-1;
   setlength(apseq,3*n);

  for i := 0 to length(seq) - 2 do      //Middle customers
  begin
    j:=j+1;
    apseq[j]:=seq[i];
    if cq<st.dems[seq[i].ID] then
    begin
      j:=j+1;
      apseq[j]:= dep;
      j:=j+1;
      apseq[j]:= seq[i];
      cq:= cq+q- st.dems[seq[i].ID];
    end
    else
    begin
      if cq=st.dems[seq[i].ID] then
      begin
        j:=j+1;
        apseq[j]:= dep;
        cq:=q;
      end
      else
      begin
      cq:=cq-st.dems[seq[i].ID];
      end;
    end;
  end;
    //Final customeer
       if cq<st.dems[seq[length(seq)-1].ID] then
      begin
        j:=j+1;
        apseq[j]:= dep;
      end;
        j:=j+1;
        apseq[j]:= seq[length(seq)-1];
        setlength(apseq,j+1);

      for i := 0 to j do aseq:=aseq+floattostr(apseq[i].id)+'-';
        
      td:= seq_length(apseq);

    Writeln('With this demand, the path without rollout is 0-'+aseq+
    '0 and its distance is ' +floattostr(td));
end;

function firstnode(seq:custarray):custarray;
var

elen,mlen:real;
i,j:integer;
aux,fnode: custarray;

begin
  mlen:=infinity;
  setlength(aux,length(seq)+1);
  setlength(fnode,length(seq));
  for i := 0 to length(seq) - 1 do
  begin
    for j := 0 to length(seq) - 1 do aux[j]:=seq[c(i+j,length(seq))];
    for j := length(aux) - 2 downto 0 do aux[j+1]:=aux[j];
    aux[0]:=dep;
    elen:= explen(aux,q,0);

    if elen< mlen then
    begin
      mlen:=elen;
      for j := 0 to length(fnode) - 1 do fnode[j] := aux[j+1];
    end;
  end;
  Writeln('Starting at customer '+floattostr(fnode[0].id)+
            ' with expected length '+floattostr(mlen));

  result:= fnode;
end;

procedure mark_visited(seq:custarray;node:customer);
var
i,j:integer;
begin
   for i := 0 to length(seq) - 1 do
      if seq[i]=node then
        for j := i to length(seq) - 2 do
        begin
        seq[j]:= seq[j+1];
      end;
    setlength(seq,length(seq)-1);
end;

function updte(cstate:state; nnode:customer; d:boolean):state;
var
nstate:state;
de:integer;

begin
  nstate :=state.create(nnode,cstate.cu_cap);

  de:= cstate.dems[nnode.ID];
  //for i:=0 to n-1 do nstate.dems[i]:=cstate.dems[i];
  nstate.dems:=cstate.dems;
  nstate.dems[nnode.ID]:=0;

  if d=false then  //New capacity
  begin
    if de>cstate.cu_cap then
    begin
      //Have to go anyway
      nstate.cu_cap:=cstate.cu_cap+q-de;
      fs:=fs+1;
      setlength(fseq,fs+1);
      fseq[fs]:=nnode;
      fs:=fs+1;
      setlength(fseq,fs+1);
      fseq[fs]:=dep;
    end
    else
    nstate.cu_cap:=cstate.cu_cap-de;
  end
  else nstate.cu_cap:= q-de;

  result:= nstate;
end;


end.
