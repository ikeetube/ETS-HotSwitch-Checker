

cbitclose(rm1, rm2, rm3); //some comments again
cbitclose(r1); //comment cbitclose(commented)
cbitclose(r1); //comment cbitclose(commented)

apu12set(APU1_R1, APU12_FV, 1.0, APU12_10V, APU12_10MA, APU12_PIN_TO_VI);
apu12set(APU2_R1, APU12_FV, 1.0, APU12_10V, APU12_10MA, APU12_PIN_TO_VI);
sp100set(SPU3_RM2, SP_FV, 1.0, SP_10V, APU12_10MA);
sp100set( SPU_R1, SP_FI, 0, SP_10V, SP_2MA );

lwait(5000);
dpinviset("DPU_RM3", DPIN_FI, -0.1, DPIN_8V, DPIN_512UA, DPIN_CLAMP_OFF, DPIN_CLAMP_OFF, MS_ALL);
apu12set(APU3_RM2, APU12_FV, 0.0, APU12_10V, APU12_10MA, APU12_PIN_TO_VI);

cbitopen(r1);
cbitopen(rm1, rm2, rm3);		