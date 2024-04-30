
Program AcyclicNetwork(input,netres);

  var
    cap:real;
    y,p,q,i,k,num,try,arcnumber:longint;
    node_i,node_j,num_arcs,num_nodes,capacity:longint;
    tail,head:longint;
    ch:char;
    done,special,sparse:boolean;
    OutFileName:string[20];
    netres:text;
    source:longint;
    sink:longint;

  Procedure WriteArc;
  Begin
    write(netres,'a');
    writeln(netres,tail:10,head:10,cap:10:0);
  End;

  Procedure AcyclicNet1;
    var ss1:real;
    Procedure NewArc1;
    Begin
      if special then
        Begin
          if (head=tail+1) then
            Begin
              ss1:=tail-num_nodes/2;
              cap:=1+sqr(ss1);
            End
          else cap:=1;
        End
      else cap:=random(capacity)+1;
      num:=try;
      try:=try+1;
      WriteArc;
    End;

  Begin                  { Procedure AcyclicNet1 }
    k:=1;   
    for p:=1 to (num_nodes-1) do
    Begin
      tail:=p;
      for q:=p+1 to num_nodes do
      Begin
        head:=q;
        NewArc1;
      End;
    End;
  End;

  Procedure AcyclicNet2;
    Procedure NewArc2;
    Begin
      if (head=tail+1) and (head<>num_nodes) then
        cap:=num_nodes
      else cap:=1;
      num:=try;
      try:=try+1;
      WriteArc;
    End;

  Begin                  { Procedure AcyclicNet2 }
    k:=1;   
    for p:=1 to (num_nodes-1) do
    Begin
      tail:=p;
      head:=p+1;
      NewArc2;
      if (head<>num_nodes) then
      Begin
        tail:=p;
        head:=num_nodes;
        NewArc2;
      End;
    End;
  End;

  Procedure Banner1;
  Begin
    writeln;
    writeln('BANNER 1');
    writeln;
  End;
  
  Procedure Banner2;
    Begin
      writeln;
      writeln('BANNER 2');
      writeln;
    End;
  
  Procedure Banner3;
   Begin
      writeln;
      writeln('BANNER 3');
      writeln;
    End;

  Procedure Banner4;
    Begin
      if not sparse then
        writeln(netres,'c Fully Dense Acyclic Network')
      else writeln(netres,'c Sparse Acyclic Network');
      writeln(netres,'c for Max-Flow');
      if not special then
        writeln(netres,'c Arcs with random capacities')
      else writeln(netres,'c Arcs with special capacities');
      writeln(netres,'p max',num_nodes:10,num_arcs:10);
      writeln(netres,'n',source:14,'  s');
      writeln(netres,'n',sink:14,'  t');
      writeln;
      writeln('  Please notice, that for simplicity');
      writeln('  the source node s is always numbered');
      writeln('  with 1, and the sink node t is');
      writeln('  assigned the largest node number,');
      writeln('  here t = ',sink,'.');
      write('  Press ENTER <ret> to continue');
      readln;
      writeln;
      writeln('  AN ACYCLIC MAX-FLOW NETWORK will');
      writeln('  be generated to file ',OutFileName,'.max.');
      writeln('  The number of nodes is  ',num_nodes:8);
      writeln('  The number of arcs is   ',num_arcs:8);
      writeln('  The source node is node ',source:8);
      writeln('  The sink node is node   ',sink:8);
      writeln;
    End;

  Procedure Banner5;
    Begin
      writeln('  The network is completed. The data');
      writeln('  file is an ASCII file, and can be');
      writeln('  accessed with your editor. You may');
      writeln('  print the file using the DOS');
      writeln('  command PRINT ',OutFileName,'.max.');
    End;

  Procedure UserValues;
    Begin
      sparse:=true;
      special:=false;
      done:=false;
      try:=1;
      writeln;
      repeat
        write('  How many nodes are in the network: ');
        readln(num_nodes);
        if (num_nodes<=1) then
        writeln('  Try again. Need at least two nodes.');
      until (num_nodes>1);
      source:=1;
      sink:=num_nodes;
      Banner2;
      writeln('  Do you want a FULLY DENSE or');
      writeln('  a SPARSE acyclic network.');
      writeln('  Type F for FULLY DENSE and S for');
      write('  SPARSE (F/S): ');
      readln(ch);
      if (ch='f') or (ch='F') then
      Begin
        sparse:=false;
        num_arcs:=0;
        for i:=1 to (num_nodes-1) do num_arcs:=num_arcs+i;
        Banner3;
        writeln('  Do you want special arc flow');
        write('  capacities (Y/N): ');
        readln(ch);
        if (ch='y') or (ch='Y') then special:=true
        else
          begin
            writeln('  What is the upper bound for arc');
            write('  FLOW CAPACITY: ');
            readln(capacity);
          end;
        Banner4;
        AcyclicNet1;
      End
      else if (ch='s') or (ch='S') then
      Begin
        num_arcs:=-1;
        for i:=2 to num_nodes do num_arcs:=num_arcs+2;
        special:=true;
        Banner4;
        AcyclicNet2;
      End;
    End;

Begin
  randomize;  {Turbo Pascal random number generator initiator.  }
              {You may have to replace this by compiler         }
              {specific randomizer, or write a short procedure. }
  Banner1;
  writeln('  Try the network generation out by');
  writeln('  following the instructions.');
  write('  Do you want to continue (Y/N) ');
  readln(ch);
  if (ch='y') or (ch='Y') then
  Begin
    write('  Enter name of the output file: ');
    readln(OutFileName);
    assign(netres,OutFileName+'.max');
    rewrite(netres);
    UserValues;
    close(netres);
    Banner5;
  End;
End.