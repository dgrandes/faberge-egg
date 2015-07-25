unit Demands;

{$MODE Delphi}

interface

type
   Demand = Class

     private
     pdmax : Integer;
     pdmin : Integer;
     pnum : Integer;

     public
     constructor Create(pdmax:integer; pdmin : integer);
     property dmax : integer read pdmax write pdmax;
     property dmin : integer read pdmin write pdmin;
     property num : integer read pnum write pnum;


end;
   implementation
   constructor demand.Create(pdmax: Integer; pdmin: Integer);
   begin
          self.dmax := pdmax;
          self.dmin := pdmin;
          self.num := pdmax-pdmin +1;
   end;
end.

