#pragma once

namespace BW
{
  /** Bitmap specifying certain unit states */
  namespace StatusFlags
  {
    enum Enum
    {
      Completed           = 0x00000001,  // 활동 가능?
      GoundedBuilding     = 0x00000002, // a building that is on the ground
      InAir               = 0x00000004,  // 지상유닛에 줘도 높이는 여전히 지상, 다만 공격/위치변경/드랍/리콜 공중판정, 건물·물 위로 이동가능
      Disabled            = 0x00000008,  /**< Protoss Unpowered */ // 가만히 있으면 유지되고 오더수행시 풀림
      Burrowed            = 0x00000010,  // 명령무시 탑승,리콜불가 오더,실드리차지,공격받음가능
      InBuilding          = 0x00000020,  // 지상유닛에 리콜시 ^2값 23으로 변함·공격가능,이동불가. 탑승시 사라짐
      InTransport         = 0x00000040,
      UNKNOWN1            = 0x00000080,  /**< @todo Unknown */ // EDIT: found in target acquisition
      RequiresDetection   = 0x00000100,  // 은폐판정, 혼자 못품
      Cloaked             = 0x00000200,  // 은폐판정, 버로·은폐로 풀림
      DoodadStatesThing   = 0x00000400,  /**< @todo Unknown */  // 디시블, 유닛 버튼셋 반응 X +명령 중지
      CloakingForFree     = 0x00000800,  /**< Requires no energy to cloak */
      CanNotReceiveOrders = 0x00001000,  // 기존 명령을 유지하나 제어불능, 오더 가능?
      NoBrkCodeStart      = 0x00002000,  /**< Unbreakable code section in iscript */  // 특정 모션 재생시?
      UNKNOWN2            = 0x00004000,  /**< @todo Unknown */
      CanNotAttack        = 0x00008000,  /**< @todo Unknown */  // 디스럽션 웹에 닿음=공격불가, 웹 없으면 사라짐
      IsAUnit             = 0x00010000,  // canAttack? /**< @todo Unknown */
      IsABuilding         = 0x00020000,
      IgnoreTileCollision = 0x00040000,  // 공중유닛? IsNormal을 뺀 지상유닛들한테 이게 더해짐.
      UNKNOWN4            = 0x00080000,  // 수송 상태의 지상유닛
      IsNormal            = 0x00100000,  /**< 1 for "normal" units, 0 for hallucinated units */ // 지상충돌판정, 없으면 지형, 건물 등 모두 통과.
      NoCollide           = 0x00200000,  // 다른 유닛이 자신과 충돌하지 않음(비콘, 버로우), 자기가 이동할 땐 아님
      UNKNOWN5            = 0x00400000,
      IsGathering         = 0x00800000,  // 채취판정, 지상충돌무시
      UNKNOWN6            = 0x01000000,
      UNKNOWN7            = 0x02000000, // Turret related
      Invincible          = 0x04000000,  // 무적 (스테이시스, 락다Timer에 제어불가 있다)
      HoldingPosition     = 0x08000000, // Set if the unit is currently holding position +벙커내 유닛
      SpeedUpgrade        = 0x10000000,  // 발업(iscript?)
      CooldownUpgrade     = 0x20000000,  // 공속업
      IsHallucination     = 0x40000000,  /**< 1 for hallucinated units, 0 for "normal" units */ // 받는 피해량 2배, 주는양 0. 스펠 맞아도 안죽음
      IsSelfDestructing   = 0x80000000  // Set for when the unit is self-destructing (scarab, scourge, infested terran)
    };
  };
};
