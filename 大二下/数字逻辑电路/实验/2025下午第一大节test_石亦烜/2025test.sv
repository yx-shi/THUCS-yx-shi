`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2025/06/06 13:15:49
// Design Name: 
// Module Name: exam
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module LFSR_random_generator(
    input wire clk,
    input wire reset,
    output wire [7:0] random_out
);

    reg [7:0] lfsr;
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            lfsr <= 8'b1;
        end else begin
            lfsr <= {lfsr[6:0], lfsr[7] ^ lfsr[5] ^ lfsr[4] ^ lfsr[3]};
        end
    end

    assign random_out = lfsr;

endmodule

module exam (
    input wire CLK,
    input wire RST,
    input wire mode,
    output reg[7:0] num,
    output reg led
);
    integer a=0;
    integer times=0;
    reg last_mode;
    reg [7:0] rand_num;
    LFSR_random_generator gen(.clk(CLK),.reset(RST),.random_out(rand_num));
    always_ff@(posedge CLK or posedge RST)begin
        if(RST==1)begin
            num<=0;
            led<=0;
            a<=0;
            times<=0;
        end
        else begin
            last_mode<=mode;
            if(last_mode==1&&mode==0)begin
                times<=times+1;
            end
                if(a<1000000)begin
                    a<=a+1;
                end
                else begin
                if(times==0)begin
                    a<=0;
                    num[2:0]<=rand_num[2:0];
                    num[5:3]<=rand_num[5:3];
                    num[7:6]<=rand_num[7:6];
                end
                else if(times==1)begin
                    a<=0;
                    num[7:6]<=num[7:6];
                    num[5:3]<=rand_num[5:3];
                    num[2:0]<=rand_num[2:0];
                end
                else if(times==2)begin
                    a<=0;
                    num[7:6]<=num[7:6];
                    num[5:3]<=num[5:3];
                    num[2:0]<=rand_num[2:0];
                end
                else begin
                    a<=0;
                    num<=num;
                    if((num[7:6]+num[5:3]+num[2:0])>=10)begin
                        led<=1;
                    end
                end 
                end
        end
    end
                        

endmodule
