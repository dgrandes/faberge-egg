unit States;

interface

uses SysUtils, Customers, Typez;

type
    state = Class

    private
     pcu_pos : customer;
     pdems : intarray;
     pcu_cap : integer;

     published
     constructor Create(pcu_pos:customer; pcu_cap: integer);
     property cu_pos : customer read pcu_pos write pcu_pos;
     property dems : intarray read pdems write pdems;
     property cu_cap : integer read pcu_cap write pcu_cap;

    End;

    statearray = array of state;

implementation

constructor state.Create(pcu_pos:customer; pcu_cap: integer);
var
i:integer;
pdems: intarray;
begin
  self.cu_pos := pcu_pos;

  setlength(pdems,n);
  for i := 0 to n - 1 do pdems[i]:=0;
  self.dems := pdems;
  self.cu_cap:= pcu_cap;

end;
end.
