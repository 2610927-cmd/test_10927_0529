import streamlit as st

# 1. 앱 페이지 설정
st.set_page_config(page_title="스마트 자판기", page_icon="🥤", layout="centered")

# 2. 세션 상태(Session State) 초기화
# 자판기의 잔액과 제품 재고/가격을 앱이 실행되는 동안 유지합니다.
if "balance" not in st.session_state:
    st.session_state.balance = 0

if "products" not in st.session_state:
    st.session_state.products = {
        "콜라 🥤": {"price": 1200, "stock": 5},
        "사이다 🍏": {"price": 1100, "stock": 3},
        "이온음료 ⚡": {"price": 1500, "stock": 4},
        "커피 ☕": {"price": 800, "stock": 8},
    }

# 3. UI 타이틀
st.title("🏪 스트림릿 미니 자판기")
st.write("돈을 넣고 원하는 음료수를 골라보세요!")
st.divider()

# 4. 왼쪽: 돈 넣기 & 현재 잔액 표시 / 오른쪽: 제품 목록 및 구매
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("💰 금액 투입")
    # 금액 투입 버튼들
    if st.button("💵 500원 투입"):
        st.session_state.balance += 500
    if st.button("💵 1,000원 투입"):
        st.session_state.balance += 1000
    
    st.markdown(f"### 현재 잔액: **{st.session_state.balance:,}원**")
    
    # 반환 버튼
    if st.button("🔄 잔액 반환하기"):
        if st.session_state.balance > 0:
            st.info(f"거스름돈 {st.session_state.balance:,}원이 반환되었습니다. 이용해 주셔서 감사합니다!")
            st.session_state.balance = 0
        else:
            st.warning("반환할 금액이 없습니다.")

with col2:
    st.subheader("🥤 음료수 메뉴")
    
    # 각 상품별로 레이아웃을 생성하여 시각화
    for name, info in st.session_state.products.items():
        price = info["price"]
        stock = info["stock"]
        
        # 상품 하나당 가로로 정렬 (이름/가격 -> 재고 -> 구매버튼)
        p_col1, p_col2, p_col3 = st.columns([2, 1, 1])
        
        with p_col1:
            st.write(f"**{name}**")
            st.caption(f"가격: {price:,}원")
            
        with p_col2:
            if stock > 0:
                st.write(f"재고: {stock}개")
            else:
                st.error("품절 ❌")
                
        with p_col3:
            # 버튼의 고유 key를 설정해 주어야 오류가 나지 않습니다.
            # 잔액이 부족하거나 재고가 없으면 버튼을 비활성화(disabled) 합니다.
            can_buy = (st.session_state.balance >= price) and (stock > 0)
            
            if st.button(f"구매", key=name, disabled=not can_buy):
                # 차감 및 재고 감소 로직
                st.session_state.balance -= price
                st.session_state.products[name]["stock"] -= 1
                st.toast(f"🎉 {name} 구매 완료!", icon="✅")
                st.rerun() # 화면을 즉시 갱신하여 잔액과 재고 수정을 반영합니다.
        
        st.write("---") # 상품 간 구분선

# 5. 하단 안내 팁
st.caption("💡 팁: 돈을 먼저 투입해야 제품 구매 버튼이 활성화됩니다.")