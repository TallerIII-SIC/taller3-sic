# def mtie_calc(phi_real, phi_arma, tau):
#     print("Length: ", len(phi_real), " and ", len(phi_arma))
#     te = phi_arma - phi_real
#     tie = te[tau:] - te[:-tau]
#     mtie = np.zeros(len(phi_arma))
#     for t_0 in range(len(phi_arma)):
#         mtie[t_0] = max(te[t_0:t_0 + tau]) - min(te[t_0:t_0 + tau])
#     return mtie