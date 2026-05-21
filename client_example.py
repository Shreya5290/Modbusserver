#!/usr/bin/env python3
"""Modbus Client Example - Verify written values from server"""

import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.defines as cst
import time

def main():
    try:
        # Connect to server
        print("=" * 60)
        print("🔌 Modbus TCP Client - Data Verification Tool")
        print("=" * 60)
        print("\nConnecting to Modbus server at 127.0.0.1:5020...")
        
        client = modbus_tcp.TcpMaster(host='127.0.0.1', port=5020)
        print("✅ Connected!\n")
        
        # Read current values
        print("📖 Reading Holding Registers (Address 0-9):")
        print("-" * 60)
        regs = client.execute(1, cst.READ_HOLDING_REGISTERS, 0, 10)
        for i, val in enumerate(regs):
            print(f"  Address {i:2d} (Register 4000{i+1:2d}): {val:5d}")
        
        # Write test values
        print("\n✍️ Writing test values [111, 222, 333] to addresses 0-2...")
        client.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[111, 222, 333])
        print("✅ Write successful!\n")
        
        # Read back immediately
        time.sleep(0.1)
        print("📖 Reading back (verify write):")
        print("-" * 60)
        regs = client.execute(1, cst.READ_HOLDING_REGISTERS, 0, 10)
        for i, val in enumerate(regs):
            status = "✅" if (i == 0 and val == 111) or (i == 1 and val == 222) or (i == 2 and val == 333) else "  "
            print(f"  {status} Address {i:2d} (Register 4000{i+1:2d}): {val:5d}")
        
        # Test coils
        print("\n🔌 Reading Coils (Address 0-9):")
        print("-" * 60)
        coils = client.execute(1, cst.READ_COILS, 0, 10)
        for i, val in enumerate(coils):
            print(f"  Address {i:2d}: {val} (ON)" if val else f"  Address {i:2d}: {val} (OFF)")
        
        # Write coil values
        print("\n✍️ Writing coil values [1, 0, 1, 0, 1] to addresses 0-4...")
        client.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 0, 1, 0, 1])
        print("✅ Write successful!\n")
        
        # Read coils back
        time.sleep(0.1)
        print("📖 Reading coils back (verify write):")
        print("-" * 60)
        coils = client.execute(1, cst.READ_COILS, 0, 10)
        for i, val in enumerate(coils):
            status = "✅" if (i in [0, 2, 4] and val) or (i in [1, 3] and not val) else "  "
            print(f"  {status} Address {i:2d}: {val} ({'ON' if val else 'OFF'})")
        
        print("\n" + "=" * 60)
        print("✅ All operations completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            client.close()
            print("\n🛑 Disconnected from server")
        except:
            pass

if __name__ == "__main__":
    main()
