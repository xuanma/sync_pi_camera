% Open cbmex first
% ... codes for cbmex open
% ...

% codes for starting Pi camera video recording are here
% On analog out port 4: ____|------...-------|____
% On analog out port 1: ______|-|_|-|..._|-|_______
cbmex('analogout', 4, 'sequence', [1,0,2400,21626,1,0], 'repeats', 1);
cbmex('analogout', 1, 'sequence', [150,0,100,21626,1,0], 'repeats', 8);
disp('Video start')

% codes for other things
% ...

% codes for stopping Pi camera video recording are here
% On analog out port 1: ____|------...-------|____
% On analog out port 4: ______|-|_|-|..._|-|_______
cbmex('analogout', 1, 'sequence', [1,0,2400,21626,1,0], 'repeats', 1);
cbmex('analogout', 4, 'sequence', [150,0,100,21626,1,0], 'repeats', 8);
disp('video stop')
pause(5)

% Close cbmex after everything is done
% ...