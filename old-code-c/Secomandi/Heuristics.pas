unit Heuristics;

  interface

  uses
  SysUtils, Math, Classes, Customers, Vehicles, Subroutines, Typez;
  function nneigh(cust : custarray): custarray;
  function _2_opt(seq:custarray):custarray;



implementation

function nneigh(cust : custarray): custarray;
var
i,j:integer;
uv : tList;
mindist : real;
seq : custarray;
curr_node : integer;
dis:real;

begin
        Writeln(' ');
        Write('The nearest neighbour sequence is 0-');

        setlength(seq,n-1);

        //Create list of unvisited nodes
        uv := Tlist.Create;
        for I := 1 to n - 1 do
        begin
            uv.add(cust[i]);
        end;
        curr_node := 0;
        i := -1;

        While uv.Count <> 0 do    //Untill all unvisited
        begin
            i := i + 1;
            mindist := infinity;
            For j :=0 to uv.Count -1 do    //find nearest unvisited neighbour
                If dist[curr_node, customer(uv[j]).ID] < mindist Then
                begin
                    mindist := dist[curr_node, customer(uv[j]).ID];
                    seq[i] := uv[j];
            end;
            curr_node := seq[i].ID;     //Add to sequence and remove from uv
            Write(inttostr(curr_node)+'-');
            uv.remove(seq[i]);
        end;
        dis:= seq_length(seq);
        Write('0 and the path distance is '+floattostr(dis));
        Result :=seq;
end;

function _2_opt(seq:custarray):custarray;
 var
 old_seq:custarray;
 i,j,k:integer;
 dis:real;
 bef,aft:real;
 changes:boolean;
 n1:integer;

  begin
    n1:=length(seq);
    setlength(old_seq,n1);
    Writeln(' ');
    Write('After 2-opt improvement, the shortest path is 0-');

    repeat
    begin
    changes:=false;
    for i := 0 to n1 - 1 do
      for j := 0 to n1 - 4 do
      begin     //c is a function that closes the cycle
        bef:=dist[seq[c(i,n1)].ID,seq[c(i+1,n1)].ID]
              +dist[seq[c(i+j+1,n1)].ID,seq[c(i+j+2,n1)].ID];
        aft:=dist[seq[c(i,n1)].ID,seq[c(i+j+1,n1)].ID]
              +dist[seq[c(i+1,n1)].ID,seq[c(i+j+2,n1)].ID];

        if aft<bef then
        begin
          changes:=true;

          //Rearrange the edges
          for k:=0 to n1-1 do old_seq[k]:= seq[k];
          seq[c(i+1,n1)]:= old_seq[c(i+j+1,n1)];
          seq[c(i+j+1,n1)]:= old_seq[c(i+1,n1)];

          //Turn around intermediate path
          for k := 1 to j - 1 do seq[c(i+1+k,n1)] :=old_seq[c(i+1+j-k,n1)] ;

        end;
      end;
    end;
     until changes=false;

    for i := 0 to n1 - 1 do Write(floattostr(seq[i].ID)+'-');
    dis:= seq_length(seq);
    Write('0 and the path distance is '+floattostr(dis));

    setlength(seq,n1+1);  //Add the depot
    for i := n1 downto 1 do seq[i]:=seq[i-1];
    seq[0]:=dep;

   result:=seq;
 end;




//Cheaper version of 2-opt.. not working yet

{function _2_opt(seq: custarray; dist : realarray) : custarray;
var
new_seq : array[0..(cust.count)] of customer ;
j,k,t1,t2,t3,t4 : integer;
changes : boolean;
cn: array of array of real;
cns :array of real;
  i: Integer;
  maxd: real;
  mind :   real;

begin
        for i := 1 to cust.Count do
        begin
          k:=0;
          mind := 999999999999999;
          maxd := 0;
          for j := 1 to cust.Count do
          begin
             if customer(cust[i]).ID <> customer(cust[j]).ID  then
             begin
                 k:=k+1;
                 cns[k]:=dist[customer(cust[i]).ID,customer(cust[j]).ID];
              end;
          end;
          Quicksort(cns, 0, k);
          cn[i]:= cns;
        end;
        {repeat
        begin
            changes = False
            For i = 1 To n
                t1 = seq(i)
                If i = n Then
                    t2 = seq(1)
                Else
                    t2 = seq(i + 1)
                End If

                Do While dist(t1, t2) > dist(t1, cn(i, k)) //Try only options fulfilling a priori cond
                    t3 = cn(i, k)
                    For z = 0 To n
                        If seq(z) = cn(i, k) Then
                            t4 = seq(z - 1)
                            j = z
                        End If
                    Next

                    If dist(t1, t2) + dist(t3, t4) > dist(t2, t3) + dist(t4, t1) Then 'Better path?
                        changes = True
                        For z = 1 To (j - i - 1)
                            new_seq(i + z) = seq(j - z)
                        Next
                        seq = new_seq
                        Exit For
                    End If
                    k = k + 1
                Loop
        end;
        until changes = False
        result := new_seq;
end;  }
end.